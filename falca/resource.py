import inspect
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable, List

import falcon
from falcon.constants import COMBINED_METHODS

from . import actions


def prepare_resource(instance: object):
    for name in dir(instance):
        method = name[3:].split("_", 1)[0].upper()
        if name.startswith("on_") and method in falcon.COMBINED_METHODS:
            func = getattr(instance, name)
            view = actions.flavor(func)
            setattr(instance, name, view)


def create_resource(methods: List[str], view_func: Callable):
    responders = {}
    for method in methods:
        assert (
            method.upper() in COMBINED_METHODS
        ), f"unknown method {method} (valid value {COMBINED_METHODS!r})"

        if iscoroutinefunction(view_func):
            # pylint: disable=unused-argument
            async def responder(self, *args, **kwds):
                return await view_func(*args, **kwds)

        else:
            # pylint: disable=unused-argument
            def responder(self, *args, **kwds):
                return view_func(*args, **kwds)

        wrapper = wraps(view_func)(responder)
        old_sig = inspect.signature(wrapper)
        params = list(inspect.signature(view_func).parameters.values())
        for param in params:
            assert (
                param.name != "self"
            ), "You cannot add the 'self' parameter to the 'view'"

        params.insert(0, inspect.Parameter("self", inspect.Parameter.POSITIONAL_ONLY))
        new_sig = old_sig.replace(parameters=params)
        responder.__signature__ = new_sig
        responders["on_" + method.lower()] = wrapper

    klass = type(view_func.__name__, (), responders)
    return klass
