import inspect
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable, List

import falcon
from falcon.constants import COMBINED_METHODS

from . import actions


def prepare_resource(klass: object):
    for name in dir(klass):
        method = name[3:].split("_", 1)[0].upper()
        if name.startswith("on_") and method in falcon.COMBINED_METHODS:
            func = getattr(klass, name)
            view = actions.flavor(func)
            setattr(klass, name, view)


def create_resource(methods: List[str], view_func: Callable):
    responders = {}
    for method in methods:
        assert (
            method.upper() in COMBINED_METHODS
        ), f"unknown method {method} (valid value {COMBINED_METHODS!r})"

        if iscoroutinefunction(view_func):

            async def responder(self, *args, **kwds):
                return await view_func(*args, **kwds)

        else:

            def responder(self, *args, **kwds):
                return view_func(*args, **kwds)

        wrapper = wraps(view_func)(responder)
        old_sig = inspect.signature(wrapper)
        params = [inspect.Parameter("self", inspect.Parameter.POSITIONAL_ONLY)] + list(
            inspect.signature(view_func).parameters.values()
        )
        new_sig = old_sig.replace(parameters=params)
        responder.__signature__ = new_sig  # boom
        responders["on_" + method.lower()] = wrapper

    klass = type(view_func.__name__, (Resource,), responders)
    return klass


class ResourceMeta(type):
    def __call__(cls, *args, **kwds):
        instance = cls.__new__(cls)
        instance.__init__(*args, **kwds)
        prepare_resource(instance)
        return instance


class Resource(metaclass=ResourceMeta):
    pass
