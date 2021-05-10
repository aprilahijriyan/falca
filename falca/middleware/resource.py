from ..helpers import get_plugins
from .base import Middleware


class ResourceMiddleware(Middleware):
    def process_resource(self, req, resp, resource, *args):
        if resource is None:
            return

        req.context.app = self.app
        req.context.templates = self.app.template_lookup
        resource.request = req
        resource.response = resp
        plugins = get_plugins(req, resource)
        for k, v in plugins.items():
            setattr(resource, k, v)
