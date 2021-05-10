import os

import falcon
from mako.lookup import TemplateLookup

from .helpers import get_root_path
from .media.json import JSONHandler, JSONHandlerWS
from .middleware.files import FileParserMiddleware
from .middleware.forms import FormParserMiddleware
from .middleware.json import JsonParserMiddleware
from .middleware.resource import ResourceMiddleware
from .plugin_manager import PluginManager
from .router import Router
from .settings import Settings


class Scaffold:
    settings_class = Settings
    plugin_manager_class = PluginManager
    router_class = Router
    media_handlers = {falcon.MEDIA_JSON: JSONHandler}

    def __init__(
        self,
        import_name,
        static_folders=[("/static", "static")],
        template_folders=["templates"],
        root_path=None,
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
        if hasattr(self, "ws_options"):
            self.ws_options.media_handlers[
                falcon.WebSocketPayloadType.TEXT
            ] = JSONHandlerWS

        self.add_middleware(ResourceMiddleware)
        self.add_middleware(FormParserMiddleware)
        self.add_middleware(JsonParserMiddleware)
        self.add_middleware(FileParserMiddleware)
        self.set_error_serializer(self.error_serializer)

    def add_middleware(self, middleware):
        super().add_middleware([middleware])

    def add_router(self, router: Router):
        assert isinstance(
            router, Router
        ), f"Router {router!r} must be an instance object of falca.router.Router"
        router.app = self
        self.routers.append(router)

    def error_serializer(self, req, resp, exc):
        resp.content_type = falcon.MEDIA_JSON
        resp.data = exc.to_json()
