from falcon.hooks import before
from falcon.routing import CompiledRouter

from . import actions


class Router(CompiledRouter):
    def __init__(self, app):
        self.app = app
        super().__init__()

    def add_route(self, uri_template: str, resource: object, **kwargs):
        def hook(req, resp, resource, params):
            req.context.app = self.app
            resource.template_lookup = self.app.template_lookup
            actions.before(req, resp, resource, params)

        resource = before(hook)(resource)
        return super().add_route(uri_template, resource, **kwargs)
