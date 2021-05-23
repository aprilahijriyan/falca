from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable

from falcon.asgi.response import Response as ASGIResponse
from falcon.asgi.ws import WebSocket
from falcon.response import Response as WSGIResponse
from typing_inspect import is_union_type

from .depends import Depends
from .helpers import get_argnotations
from .request import ASGIRequest, Request
from .responses import Response


def inject(func: Callable, *args, **kwargs):
    req_object = args[0]
    resp_object = args[1]
    params = get_argnotations(func)
    for key, atype in params.items():
        if is_union_type(atype):
            for atype in atype.__args__:
                if type(atype) is not type:
                    atype = type(atype)

                if issubclass(atype, (Request, ASGIRequest)):
                    kwargs[key] = req_object

                elif issubclass(atype, (WSGIResponse, ASGIResponse)) and isinstance(
                    resp_object, (WSGIResponse, ASGIResponse)
                ):
                    kwargs[key] = resp_object

                elif issubclass(atype, WebSocket) and isinstance(
                    resp_object, WebSocket
                ):
                    kwargs[key] = resp_object

            continue

        elif isinstance(atype, Depends):
            rv = inject(atype, *args, **kwargs)
            kwargs[key] = rv

        if type(atype) is not type:
            atype = type(atype)

        if issubclass(atype, (Request, ASGIRequest)):
            kwargs[key] = req_object

        elif issubclass(atype, (WSGIResponse, ASGIResponse)) and isinstance(
            resp_object, (WSGIResponse, ASGIResponse)
        ):
            kwargs[key] = resp_object

        elif issubclass(atype, WebSocket) and isinstance(resp_object, WebSocket):
            kwargs[key] = resp_object

    if isinstance(func, Depends):
        return func(*args[2:], **kwargs)

    return kwargs


def flavor(func: Callable):
    if iscoroutinefunction(func):

        async def responder(*args, **kwargs):
            kwargs = inject(func, *args, **kwargs)
            resp = await func(*args[2:], **kwargs)
            if isinstance(resp, Response):
                resp.build(args[0], args[1])

    else:

        def responder(*args, **kwargs):
            kwargs = inject(func, *args, **kwargs)
            resp = func(*args[2:], **kwargs)
            if isinstance(resp, Response):
                resp.build(args[0], args[1])

    wrapper = wraps(func)(responder)
    return wrapper
