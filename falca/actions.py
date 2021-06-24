from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable, Union

from falcon.asgi.response import Response as ASGIResponse
from falcon.asgi.ws import WebSocket
from falcon.response import Response as WSGIResponse
from typing_inspect import is_union_type

from .depends import Depends
from .helpers import get_argnotations
from .request import ASGIRequest, Request
from .responses import Response


def _get_hint_object(
    atype: object,
    req_object: Union[Request, ASGIRequest],
    resp_object: Union[WSGIResponse, ASGIResponse, WebSocket],
):
    if type(atype) is not type:
        atype = type(atype)

    if issubclass(atype, (Request, ASGIRequest)):
        return req_object

    elif issubclass(atype, (WSGIResponse, ASGIResponse, WebSocket)) and isinstance(
        resp_object, (WSGIResponse, ASGIResponse, WebSocket)
    ):
        return resp_object


def inject(func: Callable, *args, **kwargs):
    req_object = args[0]
    resp_object = args[1]
    params = get_argnotations(func)
    for key, atype in params.items():
        if is_union_type(atype):
            for atype in atype.__args__:
                kwargs[key] = _get_hint_object(atype, req_object, resp_object)

        elif isinstance(atype, Depends):
            rv = inject(atype, *args, **kwargs)
            kwargs[key] = rv

        else:
            kwargs[key] = _get_hint_object(atype, req_object, resp_object)

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
