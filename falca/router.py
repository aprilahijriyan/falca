from falcon.app import App
from falcon.routing import CompiledRouter


class Router(CompiledRouter):
    def __init__(self, app: App = None, *, url_prefix: str = None):
        self.app = app
        self.url_prefix = url_prefix
        super().__init__()

    def add_route(self, uri_template: str, resource: object, **kwargs):
        if self.url_prefix:
            uri_template = self.url_prefix + uri_template

        return super().add_route(uri_template, resource, **kwargs)

    def find(self, uri: str, req=None):
        resource = super().find(uri, req=req)
        if resource is None:
            for router in self.app.routers:
                resource = router.find(uri, req=req)
                if resource:
                    break
        return resource


class AsyncRouter(Router):
    def add_route(self, uri_template: str, resource: object, **kwargs):
        kwargs["_asgi"] = True
        return super().add_route(uri_template, resource, **kwargs)
