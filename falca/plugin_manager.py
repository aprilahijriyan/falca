from .helpers import import_attr


class PluginManager:
    def __init__(self, app) -> None:
        self.app = app
        self.plugins = {}

    def has(self, name):
        return name in self.plugins

    def get(self, name):
        return self.plugins.get(name)

    def install(self, name: str, src: str):
        plugin = import_attr(src)
        self.plugins[name] = plugin(self.app)

    def uninstall(self, name: str):
        del self.plugins[name]
