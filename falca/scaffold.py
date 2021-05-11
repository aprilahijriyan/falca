import os
from typing import List, Tuple

import falcon
from falcon.asgi import App as ASGIApp
from falcon.asgi.request import Request as ASGIRequest
from falcon.asgi.response import Response as ASGIResponse
from mako.lookup import TemplateLookup
from marshmallow.exceptions import ValidationError

from .helpers import get_http_description, get_root_path
from .media.json import JSONHandler, JSONHandlerWS
from .middleware.files import FileParserMiddleware
from .middleware.forms import FormParserMiddleware
from .middleware.json import JsonParserMiddleware
from .middleware.resource import ResourceMiddleware
from .plugin_manager import PluginManager
from .router import AsyncRouter, Router
from .settings import Settings


class Scaffold:
    settings_class = Settings
    plugin_manager_class = PluginManager
    router_class = Router
    media_handlers = {falcon.MEDIA_JSON: JSONHandler}

    def __init__(
        self,
        import_name: str,
        static_folders: List[Tuple[str, str]] = [("/static", "static")],
        template_folders: List[str] = ["templates"],
        root_path: str = None,
        **kwds,
    ) -> None:
        self.import_name = import_name
        self._router = self.router_class(self)
        self._router_search = self._router.find
        self.settings = self.settings_class()
        self.static_folders = static_folders
        if root_path is None:
            root_path = get_root_path(import_name)

        self.root_path = root_path
        self.routers = []
        templates = []
        for t in template_folders:
            if not t.startswith("/"):
                t = os.path.join(root_path, t)
            templates.append(t)

        templates.insert(0, os.path.join(os.path.dirname(__file__), "templates"))
        self.template_folders = templates
        self.template_lookup = TemplateLookup(templates)
        self.plugin_manager = self.plugin_manager_class(self)
        for prefix, folder in static_folders:
            if not folder.startswith("/"):
                folder = os.path.join(root_path, folder)

            self.add_static_route(prefix, folder)

        # rfc: https://falcon.readthedocs.io/en/latest/api/media.html#replacing-the-default-handlers
        self.req_options.media_handlers.update(self.media_handlers)
        self.resp_options.media_handlers.update(self.media_handlers)
        m_handler = self.marshmallow_handler
        if isinstance(self, ASGIApp):
            self.ws_options.media_handlers[
                falcon.WebSocketPayloadType.TEXT
            ] = JSONHandlerWS
            m_handler = self.marshmallow_handler_async

        self.add_middleware(ResourceMiddleware(self))
        self.add_middleware(FormParserMiddleware(self))
        self.add_middleware(JsonParserMiddleware(self))
        self.add_middleware(FileParserMiddleware(self))
        self.set_error_serializer(self.error_serializer)
        self.add_error_handler(ValidationError, m_handler)

    def add_router(self, router: Router):
        if isinstance(self, ASGIApp):
            assert (
                type(router) is AsyncRouter
            ), f"Router {router!r} must be an instance object of falca.router.AsyncRouter"
        else:
            assert (
                type(router) is Router
            ), f"Router {router!r} must be an instance object of falca.router.Router"

        router.app = self
        self.routers.append(router)

    def error_serializer(
        self, req: falcon.Request, resp: falcon.Response, exc: falcon.HTTPError
    ):
        resp.content_type = falcon.MEDIA_JSON
        resp.data = exc.to_json()

    def marshmallow_handler(
        self, req: falcon.Request, resp: falcon.Response, exc: ValidationError, *args
    ):
        resp.status = falcon.HTTP_422
        resp.content_type = falcon.MEDIA_JSON
        resp.media = {
            "status": {"code": 422, "detail": get_http_description(422)},
            "data": exc.messages,
        }

    async def marshmallow_handler_async(
        self, req: ASGIRequest, resp: ASGIResponse, exc: ValidationError, *args
    ):
        self.marshmallow_handler(req, resp, exc, *args)
