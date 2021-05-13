from typing import List, Union

from falcon.routing import CompiledRouter


class Router(CompiledRouter):
    def __init__(self, *, url_prefix: str = None):
        self.url_prefix = url_prefix
        self.children: List[Router] = []
        super().__init__()

    def add_route(self, uri_template: str, resource: object, **kwargs):
        if self.url_prefix:
            uri_template = self.url_prefix + uri_template

        return super().add_route(uri_template, resource, **kwargs)

    def include_router(self, router: Union["Router", "AsyncRouter"]):
        self.children.append(router)

    def find(self, uri: str, req=None):
        resource = super().find(uri, req=req)
        if resource is None:
            for router in self.children:
                resource = router.find(uri, req=req)
                if resource:
                    break
        return resource


class AsyncRouter(Router):
    def add_route(self, uri_template: str, resource: object, **kwargs):
        kwargs["_asgi"] = True
        return super().add_route(uri_template, resource, **kwargs)
