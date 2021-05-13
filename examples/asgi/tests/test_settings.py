from os import environ

from settings import Config, full_config, part_config

from falca.settings import Settings


def test_from_object(settings: Settings):
    settings.from_object(Config)
    assert settings == full_config
    settings.from_object("settings.Config")
    assert settings == full_config


def test_from_envvar(settings: Settings):
    envvar = "FALCA_SETTINGS"
    environ[envvar] = "settings"
    settings.from_envvar(envvar)
    assert list(settings.keys()) == ["part_config", "full_config", "Config"]


def test_settings_with_prefixes(settings: Settings):
    prefix = "FALCA_"
    settings.from_object(Config, prefix=prefix)
    assert settings == part_config
