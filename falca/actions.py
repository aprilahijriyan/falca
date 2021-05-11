from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable

from .annotations import Annotation
from .helpers import get_argnotations, get_plugins


def flavor(func: Callable):
    _cache = {}

    def logic(*args, **kwargs):
        req_object = args[0]
        plugins = _cache.get("plugins", {})
        if not plugins:
            plugins = get_plugins(req_object, func)
            _cache["plugins"] = plugins

        kwargs.update(plugins)
        args = args[2:]  # without req, resp
        params = get_argnotations(func)
        for key, atype in params.items():
            if isinstance(atype, Annotation):
                atype.load(req_object)
                kwargs[key] = atype

        return args, kwargs

    if iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            args, kwargs = logic(*args, **kwargs)
            await func(*args, **kwargs)

    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            args, kwargs = logic(*args, **kwargs)
            func(*args, **kwargs)

    return wrapper
