import os
from functools import partialmethod
from typing import List, Tuple, Union

from falcon.asgi import App as ASGIApp
from falcon.constants import MEDIA_JSON, WebSocketPayloadType
from mako.lookup import TemplateLookup
from typer import Typer

from . import handlers
from .exceptions import FalcaError
from .helpers import get_root_path
from .media.json import JSONHandler, JSONHandlerWS
from .middleware.files import FileParserMiddleware
from .middleware.forms import FormParserMiddleware
from .middleware.json import JsonParserMiddleware
from .middleware.resource import ResourceMiddleware
from .plugins.manager import PluginManager
from .router import AsyncRouter, Router
from .settings import Settings


class Scaffold:
    settings_class = Settings
    plugins_class = PluginManager
    router_class = Router
    cli_class = Typer
    media_handlers = {MEDIA_JSON: JSONHandler}

    def __init__(
        self,
        import_name: str,
        static_folders: List[Tuple[str, str]] = [("/static", "static")],
        template_folders: List[str] = ["templates"],
        root_path: str = None,
        **kwds,
    ) -> None:
        self.import_name = import_name
        self._router: Router = self.router_class()
        self._router_search = self._router.find
        self.settings = self.settings_class()
        self.static_folders = static_folders
        if root_path is None:
            root_path = get_root_path(import_name)

        self.root_path = root_path
        templates = []
        for t in template_folders:
            if not t.startswith("/"):
                t = os.path.join(root_path, t)
            templates.append(t)

        templates.insert(0, os.path.join(os.path.dirname(__file__), "templates"))
        self.template_folders = templates
        self.template_lookup = TemplateLookup(templates)
        self.plugins = self.plugins_class(self)
        for prefix, folder in static_folders:
            if not folder.startswith("/"):
                folder = os.path.join(root_path, folder)

            self.add_static_route(prefix, folder)

        self.cli = self.cli_class(name=import_name)
        # rfc: https://falcon.readthedocs.io/en/latest/api/media.html#replacing-the-default-handlers
        self.req_options.media_handlers.update(self.media_handlers)
        self.resp_options.media_handlers.update(self.media_handlers)
        if isinstance(self, ASGIApp):
            self.ws_options.media_handlers[WebSocketPayloadType.TEXT] = JSONHandlerWS

        self.apps = {}
        self.add_middleware(ResourceMiddleware(self))
        self.add_middleware(FormParserMiddleware())
        self.add_middleware(JsonParserMiddleware())
        self.add_middleware(FileParserMiddleware())
        self._set_default_error_handlers()

    def route(self, path: str, methods: List[str] = ["get", "head"]):
        def decorated(func):
            self._router.route(path, methods)(func)
            return func

        return decorated

    head = partialmethod(route, methods=["head"])
    get = partialmethod(route, methods=["get"])
    post = partialmethod(route, methods=["post"])
    put = partialmethod(route, methods=["put"])
    delete = partialmethod(route, methods=["delete"])
    options = partialmethod(route, methods=["options"])
    patch = partialmethod(route, methods=["patch"])
    trace = partialmethod(route, methods=["trace"])

    def include_router(self, router: Union[Router, AsyncRouter]):
        if isinstance(self, ASGIApp):
            assert (
                type(router) is AsyncRouter
            ), f"Router {router!r} must be an instance object of falca.router.AsyncRouter"
        else:
            assert (
                type(router) is Router
            ), f"Router {router!r} must be an instance object of falca.router.Router"

        self._router.include_router(router)

    def mount(self, path: str, app: "Scaffold"):
        if path in self.apps:
            raise FalcaError(f"Application is already registered with path {path}")

        self.apps[path] = app

    def find_app(self, env: dict):
        key = "PATH_INFO" if not isinstance(self, ASGIApp) else "path"
        path_info = env.get(key, "")
        if not path_info:
            return

        for path, app in self.apps.items():
            if path_info.startswith(path):
                path_info = "/" + path_info.replace(path, "", 1).lstrip("/")
                env[key] = path_info
                return app

    def make_shell_context(self):
        return {
            "app": self,
            "router": self._router,
            "plugins": self.plugins,
            "templates": self.template_lookup,
        }

    def _set_default_error_handlers(self):
        self.set_error_serializer(handlers.http_handler)
        exc = handlers.MarshmallowValidationError
        if exc:
            if isinstance(self, ASGIApp):
                self.add_error_handler(exc, handlers.marshmallow_handler_async)
            else:
                self.add_error_handler(exc, handlers.marshmallow_handler)

        exc = handlers.PydanticValidationError
        if exc:
            if isinstance(self, ASGIApp):
                self.add_error_handler(exc, handlers.pydantic_handler_async)
            else:
                self.add_error_handler(exc, handlers.pydantic_handler)
