from falcon.hooks import before
from falcon.routing import CompiledRouter

from . import actions


class Router(CompiledRouter):
    def __init__(self, app=None, *, url_prefix: str = None):
        self.app = app
        self.url_prefix = url_prefix
        super().__init__()

    def add_route(self, uri_template: str, resource: object, **kwargs):
        def hook(req, resp, resource, params):
            req.context.app = self.app
            resource.template_lookup = self.app.template_lookup
            resource.request = req
            resource.response = resp
            actions.before(req, resp, resource, params)

        if self.url_prefix:
            uri_template = self.url_prefix + uri_template

        resource = before(hook)(resource)
        return super().add_route(uri_template, resource, **kwargs)

    def find(self, uri, req=None):
        resource = super().find(uri, req=req)
        if resource is None:
            for router in self.app.routers:
                resource = router.find(uri, req=req)
                if resource:
                    break
        return resource
