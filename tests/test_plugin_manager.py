from pytest import raises

from falca.exceptions import PluginError
from falca.plugins.base import BasePlugin


def test_get_plugin(wsgi_app):
    with raises(PluginError):
        wsgi_app.plugins.get("not_found")


def test_install_plugin(wsgi_app):
    wsgi_app.plugins.install("tests.test_depends.Logger")


def test_bad_plugin(wsgi_app):
    class Plugin:
        pass

    with raises(PluginError) as info:
        wsgi_app.plugins.install(Plugin)
        exc = info.value
        assert "invalid plugin object" in exc.args[0]

    class Plugin(BasePlugin):
        pass

    with raises(PluginError) as info:
        wsgi_app.plugins.install(Plugin)
        exc = info.value
        assert "plugin name is required" in exc.args[0]


def test_uninstall_plugin(wsgi_app):
    class Plugin(BasePlugin):
        name = "test"

    wsgi_app.plugins.install(Plugin)
    wsgi_app.plugins.uninstall("test")
