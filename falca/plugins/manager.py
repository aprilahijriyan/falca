from typing import Dict, Union

from falcon.app import App

from ..exceptions import PluginError
from ..helpers import import_attr
from .base import BasePlugin


class PluginManager:
    def __init__(self, app: App) -> None:
        self.app = app
        self.storage: Dict[str, BasePlugin] = {}

    def has(self, name: str):
        return name in self.storage

    def get(self, name: str):
        if not self.has(name):
            raise PluginError(f"plugin {name!r} not found")
        return self.storage.get(name)

    def install(self, src: Union[object, str], name: str = None):
        plugin = src
        if isinstance(src, str):
            plugin = import_attr(plugin)

        if not issubclass(plugin, BasePlugin):
            raise PluginError(f"invalid plugin object {plugin}")

        name = name or plugin.name
        if not name:
            raise PluginError("plugin name is required")

        self.storage[name] = plugin(self.app)

    def uninstall(self, name: str):
        del self.storage[name]
