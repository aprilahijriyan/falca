from typing import List, Union

from falcon.routing import CompiledRouter


class Router(CompiledRouter):
    def __init__(self, *, url_prefix: str = None):
        self.url_prefix = url_prefix
        self.children: List[Router] = []
        self._uri_mapping = []
        super().__init__()

    def add_route(self, uri_template: str, resource: object, **kwargs):
        if self.url_prefix:
            uri_template = self.url_prefix + uri_template

        self._check_endpoint(uri_template)
        self._uri_mapping.append(uri_template)
        return super().add_route(uri_template, resource, **kwargs)

    def _check_endpoint(self, uri_template: str):
        assert (
            uri_template not in self._uri_mapping
        ), f"Endpoint {uri_template!r} already exists"

    def include_router(self, router: Union["Router", "AsyncRouter"]):
        assert router.url_prefix, "URL prefix needed for nesting router"
        self._check_router(router)
        self.children.append(router)

    def _check_router(self, router: Union["Router", "AsyncRouter"]):
        for r in self.children:
            assert router.url_prefix != r.url_prefix, "Router already exists"

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
