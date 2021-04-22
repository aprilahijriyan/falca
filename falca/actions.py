import falcon

from .exceptions import PluginNotFound
from .helpers import extract_plugins, isclass


def before(req, resp, resource, params):
    print("Resource:", resource)
    plugins = {}
    manager = req.context.app.plugin_manager
    for name in extract_plugins(resource):
        plugin = manager.get(name)
        if not plugin:
            raise PluginNotFound(name)

        plugins[name] = plugin

    params.update(plugins)

    if isclass(resource):
        for p, v in plugins.items():
            setattr(resource, p, v)
    else:
        params.update(plugins)
