from .base import BaseLoader


class PluginLoader(BaseLoader):
    def load(self):
        plugins: dict = self.app.settings.get("PLUGINS", {})
        plugin_manager = self.app.plugin_manager
        for name, src in plugins.items():
            plugin_manager.install(name, src)
