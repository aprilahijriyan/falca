from typing import Union

from falcon.asgi.request import Request as ASGIRequest
from falcon.asgi.response import Response as ASGIResponse
from falcon.asgi.ws import WebSocket
from falcon.response import Response

from ..helpers import get_plugins
from ..request import ASGIRequest, Request
from .base import Middleware


class ResourceMiddleware(Middleware):
    def process_resource(
        self, req: Request, resp: Union[Response, WebSocket], resource: object, *args
    ):
        if resource is None:
            return

        req.context.app = self.app
        req.context.templates = self.app.template_lookup
        plugins = getattr(resource, "_cached_plugins", False)
        if not plugins:
            plugins = get_plugins(req, resource)
            for k, v in plugins.items():
                setattr(resource, k, v)
            resource._cached_plugins = True

    async def process_resource_async(
        self, req: ASGIRequest, resp: ASGIResponse, resource: object, *args
    ):
        self.process_resource(req, resp, resource, *args)

    async def process_resource_ws(
        self, req: ASGIRequest, ws: WebSocket, resource: object, params: dict
    ):
        return self.process_resource(req, ws, resource, params)
