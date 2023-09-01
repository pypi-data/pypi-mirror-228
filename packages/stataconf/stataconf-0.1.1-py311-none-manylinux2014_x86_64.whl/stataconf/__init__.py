"""What if Jason tried to solve the configuration problem?"""
__version__ = "0.1.1"

from abc import ABC, abstractmethod
import collections
import os
import pathlib
import shutil
import subprocess
import tempfile
import tomllib
import typing
import urllib.parse

from smart_open import open as smart_open


class StataInternalConf(collections.UserDict):
    def __getitem__(self, key):
        if not isinstance(key, str):
            raise ValueError("`StataInternalConf` expects str as key")
        return collections.UserDict.__getitem__(self, key.lower())

    def __setitem__(self, key, val):
        if not isinstance(key, str):
            raise ValueError("`StataInternalConf` expects str as key")
        collections.UserDict.__setitem__(self, key.lower(), val)


STATA_CONF_KEY_TYPE = str
STATA_CONF_VALUE_TYPE = str

STATA_BUILD_STEP = typing.Callable[
    [StataInternalConf],
    typing.Iterable[typing.Tuple[STATA_CONF_KEY_TYPE, STATA_CONF_VALUE_TYPE]],
]


def run_stata_loaders(
    stata_loaders: typing.Sequence["StataLoader"],
) -> StataInternalConf:
    builder = StataBuilder()
    for stata_loader in reversed(stata_loaders):
        builder = stata_loader.make_builder(builder)
    return builder.build()


class StataBuilder(object):
    def __init__(self, build_step: typing.Optional[STATA_BUILD_STEP] = None):
        self._build_step = build_step

    def _noop_build_step(
        self, current_conf: StataInternalConf
    ) -> typing.Iterable[typing.Tuple[STATA_CONF_KEY_TYPE, STATA_CONF_VALUE_TYPE]]:
        yield from current_conf.items()

    def build_step(
        self, current_conf: StataInternalConf
    ) -> typing.Iterable[typing.Tuple[STATA_CONF_KEY_TYPE, STATA_CONF_VALUE_TYPE]]:
        if self._build_step:
            yield from self._build_step(current_conf)
        else:
            yield from self._noop_build_step(current_conf)

    def build(
        self, current_conf: typing.Optional[StataInternalConf] = None
    ) -> StataInternalConf:
        if current_conf is None:
            current_conf = StataInternalConf()
        return StataInternalConf(self.build_step(current_conf))


class StataLoader(ABC):
    @abstractmethod
    def make_builder(self, next_builder: "StataBuilder") -> "StataBuilder":
        pass


class StataConf(object):
    def __init__(self, stata_loaders: typing.Sequence[StataLoader]):
        self._stata_loaders = stata_loaders
        self._internal_conf = run_stata_loaders(self._stata_loaders)

    def __getitem__(self, name: str):
        if not isinstance(name, str):
            raise StataException("`StataConf` keys are strings.")
        return self._internal_conf[name.lower()]

    def __setitem__(self, name, value):
        raise StataException(
            "You can't mutate a `StataConf`: it's static (hint: it's in the name)."
        )


class EnvStataLoader(StataLoader):
    def __init__(
        self, *, prefix: str, whitelist: typing.Optional[typing.Sequence[str]] = None
    ):
        self._prefix = prefix
        self._whitelist = whitelist

    def make_builder(self, next_builder: "StataBuilder") -> "StataBuilder":
        def build_step(current_conf: StataInternalConf):
            local_conf = StataInternalConf(**current_conf)
            for env_key, env_value in os.environ.items():
                if env_key.startswith(self._prefix):
                    conf_key = env_key.removeprefix(self._prefix)
                    if self._whitelist is None or conf_key in self._whitelist:
                        local_conf[env_key.removeprefix(self._prefix)] = env_value
            yield from next_builder.build_step(local_conf)

        return StataBuilder(build_step)


class StataException(Exception):
    pass


def get_url_content(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    scheme = parsed_url.scheme
    if parsed_url.scheme in ["file", "s3"]:
        try:
            with smart_open(url) as f:
                return f.read()
        except Exception as error:
            raise StataException(f'Could not read URL "{url}"') from error
    raise StataException(f'Unrecognized URL scheme "{scheme}"')


def _inner_lower_dict_keys(a_dict):
    for key, value in a_dict.items():
        yield key.lower(), _lower_dict_keys(value) if isinstance(value, dict) else value


def _lower_dict_keys(a_dict):
    return dict(_inner_lower_dict_keys(a_dict))


class TomlStataLoader(StataLoader):
    def __init__(self, *, url: str):
        self._url = url

    def make_builder(self, next_builder: "StataBuilder") -> "StataBuilder":
        def build_step(current_conf: StataInternalConf):
            raw_config = get_url_content(self._url)
            config = tomllib.loads(raw_config)
            local_conf = StataInternalConf(**current_conf, **_lower_dict_keys(config))
            yield from next_builder.build_step(local_conf)

        return StataBuilder(build_step)


class SopsProtectedTomlStataLoader(StataLoader):
    def __init__(self, *, url: str, local_cache: bool = False):
        self._url = url
        self._local_cache = local_cache

    def make_builder(self, next_builder: "StataBuilder") -> "StataBuilder":
        def build_step(current_conf: StataInternalConf):
            raw_config = get_url_content(self._url)

            sops_binary = "sops"
            if shutil.which(sops_binary) is None:
                sops_binary = str(
                    pathlib.PurePath(__file__).parent.joinpath(
                        # FIXME: It can be darwin.arm64
                        "sops-v3.7.3.linux.amd64"
                    )
                )

            with tempfile.TemporaryDirectory() as d:
                cyphertext_path = pathlib.PurePath(d).joinpath("cyphertext")
                with open(cyphertext_path, "w") as f:
                    f.write(raw_config)
                completed_process = subprocess.run(
                    [sops_binary, "-d", cyphertext_path], capture_output=True
                )

            if completed_process.returncode != 0:
                raise StataException(
                    f"`sops` failed with exit code {completed_process.returncode}. Stderr was: "
                    + completed_process.stderr.decode("utf-8")
                )

            config = tomllib.loads(completed_process.stdout.decode("utf-8"))
            local_conf = StataInternalConf(**current_conf, **_lower_dict_keys(config))
            yield from next_builder.build_step(local_conf)

        return StataBuilder(build_step)
