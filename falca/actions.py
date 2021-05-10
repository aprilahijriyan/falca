from functools import wraps
from typing import Callable

from falcon.request import Request
from falcon.response import Response

from .annotations import Annotation
from .exceptions import PluginNotFound
from .helpers import extract_plugins, get_argnotations, isclass


def before(req: Request, resp: Response, resource: object, params: dict):
    print("before hook")
    plugins = {}
    manager = req.context.app.plugin_manager
    for name in extract_plugins(resource):
        plugin = manager.get(name)
        if not plugin:
            raise PluginNotFound(name)

        plugins[name] = plugin

    if isclass(resource):
        for p, v in plugins.items():
            setattr(resource, p, v)
    else:
        params.update(plugins)


def flavor(func: Callable):
    @wraps(func)
    def decorated(*args, **kwargs):
        print("Decorated:", args)
        req_object = args[0]
        args = args[2:]  # without req, resp
        params = get_argnotations(func)
        for key, atype in params.items():
            if isinstance(atype, Annotation):
                atype.load(req_object)
                kwargs[key] = atype

        func(*args, **kwargs)

    return decorated
