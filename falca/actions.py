from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable

from falcon.asgi.response import Response as ASGIResponse
from falcon.response import Response as WSGIResponse

from .annotations import Annotation
from .helpers import get_argnotations, get_plugins
from .request import ASGIRequest, Request
from .responses import Response


def flavor(func: Callable):
    _cache = {}

    def logic(*args, **kwargs):
        req_object = args[0]
        resp_object = args[1]
        plugins = _cache.get("plugins", {})
        if not plugins:
            plugins = get_plugins(req_object, func)
            _cache["plugins"] = plugins

        kwargs.update(plugins)
        params = get_argnotations(func)
        for key, atype in params.items():
            if isinstance(atype, Annotation):
                atype.load(req_object)
                kwargs[key] = atype

            elif issubclass(atype, (Request, ASGIRequest)):
                kwargs[key] = req_object

            elif issubclass(atype, (WSGIResponse, ASGIResponse)):
                kwargs[key] = resp_object

        return kwargs

    if iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            kwargs = logic(*args, **kwargs)
            resp = await func(*args[2:], **kwargs)
            if isinstance(resp, Response):
                resp.build(args[0], args[1])

    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs = logic(*args, **kwargs)
            resp = func(*args[2:], **kwargs)
            if isinstance(resp, Response):
                resp.build(args[0], args[1])

    return wrapper
