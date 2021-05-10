from ..actions import before
from .base import Middleware


class ResourceMiddleware(Middleware):
    def process_resource(self, req, resp, resource, *args):
        req.context.app = self.app
        req.context.templates = self.app.template_lookup
        resource.request = req
        resource.response = resp
        before(req, resp, resource, {})
