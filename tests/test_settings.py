from os import environ

from .settings import Config, full_config, part_config


def test_from_object(wsgi_app):
    settings = wsgi_app.settings
    settings.clear()
    settings.from_object(Config)
    assert settings == full_config
    settings.from_object("tests.settings.Config")
    assert settings == full_config


def test_from_envvar(wsgi_app):
    settings = wsgi_app.settings
    settings.clear()
    envvar = "FALCA_SETTINGS"
    environ[envvar] = "tests.settings"
    settings.from_envvar(envvar)
    assert list(settings.keys()) == ["part_config", "full_config", "Config"]


def test_settings_with_prefixes(wsgi_app):
    settings = wsgi_app.settings
    settings.clear()
    prefix = "FALCA_"
    settings.from_object(Config, prefix=prefix)
    assert settings == part_config
