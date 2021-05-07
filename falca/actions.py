from functools import wraps
from typing import Callable

from falcon.request import Request
from falcon.response import Response

from .annotations import File, Form, Header, Query
from .exceptions import PluginNotFound
from .helpers import extract_plugins, get_argnotations, isclass

SPECIAL_ARGUMENTS = (Query, Form, File, Header)


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
        req_object = args[1]
        args = [args[0]] + args[3:]  # without req, resp
        raise Exception(req_object, args)
        params = get_argnotations(func)
        for key, atype in params.items():
            if isinstance(atype, SPECIAL_ARGUMENTS):
                atype.load(req_object)
                kwargs[key] = atype

        func(*args, **kwargs)

    return decorated
