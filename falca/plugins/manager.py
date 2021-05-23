from falcon.app import App

from ..helpers import import_attr


class PluginManager:
    def __init__(self, app: App) -> None:
        self.app = app
        self.storage = {}

    def has(self, name: str):
        return name in self.storage

    def get(self, name: str):
        return self.storage.get(name)

    def install(self, name: str, src: str):
        plugin = import_attr(src)
        self.storage[name] = plugin(self.app)

    def uninstall(self, name: str):
        del self.storage[name]
