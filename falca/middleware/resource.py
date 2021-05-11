from falcon.request import Request
from falcon.response import Response

from ..helpers import get_plugins
from .base import Middleware


class ResourceMiddleware(Middleware):
    def process_resource(self, req: Request, resp: Response, resource: object, *args):
        if resource is None:
            return

        req.context.app = self.app
        req.context.templates = self.app.template_lookup
        resource.request = req
        resource.response = resp
        plugins = getattr(resource, "_cached_plugins", False)
        if not plugins:
            plugins = get_plugins(req, resource)
            for k, v in plugins.items():
                setattr(resource, k, v)
            resource._cached_plugins = True
