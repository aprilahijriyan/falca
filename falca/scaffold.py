import os

import falcon
from mako.lookup import TemplateLookup

from .helpers import get_root_path
from .media.json import JSONHandler, JSONHandlerWS
from .plugin_manager import PluginManager
from .router import Router
from .settings import Settings


class Scaffold:
    settings_class = Settings
    plugin_manager_class = PluginManager
    router_class = Router
    media_handlers = {falcon.MEDIA_JSON: JSONHandler}
    default_settings = {
        "STATICFILES": [],
        "TEMPLATES_DIR": [],
        "PLUGINS": {"openapi": "falca.openapi.OpenAPI"},
    }

    def __init__(
        self,
        import_name,
        static_folders=[("/static", "static")],
        template_folders=["templates"],
        root_path=None,
        **kwds
    ) -> None:
        self.import_name = import_name
        router = self.router_class(self)
        kwds["router"] = router
        super().__init__(**kwds)
        self.settings = self.settings_class()
        self.settings.from_dict(self.default_settings)
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
        self.plugin_manager = self.plugin_manager_class(self)
        # rfc: https://falcon.readthedocs.io/en/latest/api/media.html#replacing-the-default-handlers
        self.req_options.media_handlers.update(self.media_handlers)
        self.resp_options.media_handlers.update(self.media_handlers)
        self.ws_options.media_handlers[falcon.WebSocketPayloadType.TEXT] = JSONHandlerWS
        for prefix, folder in static_folders:
            if not folder.startswith("/"):
                folder = os.path.join(root_path, folder)

            self.add_static_route(prefix, folder)
