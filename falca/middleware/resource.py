from .base import Middleware


class ResourceMiddleware(Middleware):
    def process_resource(self, req, resp, resource, *args):
        print("resource midd:", req, resp, resource)
        req.context.app = self.app
        req.context.templates = self.app.template_lookup
        resource.request = req
        resource.response = resp
