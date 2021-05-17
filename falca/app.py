from functools import partialmethod

from falcon.app import App as WSGIBase
from falcon.asgi import App as ASGIBase

from .request import ASGIRequest, Request
from .router import AsyncRouter
from .scaffold import Scaffold


class WSGI(WSGIBase, Scaffold):
    def __init__(self, import_name: str, **kwds):
        kwds["request_type"] = Request
        super().__init__(**kwds)
        Scaffold.__init__(self, import_name, **kwds)


class ASGI(ASGIBase, Scaffold):
    router_class = AsyncRouter

    def __init__(self, import_name: str, **kwds):
        kwds["request_type"] = ASGIRequest
        super().__init__(**kwds)
        Scaffold.__init__(self, import_name, **kwds)

    websocket = partialmethod(Scaffold.route, methods=["websocket"])
