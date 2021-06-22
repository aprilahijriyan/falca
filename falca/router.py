from functools import partialmethod
from typing import Callable, List, Optional, Union

from falcon.routing import CompiledRouter

from .exceptions import BadRouter, EndpointConflict, FalcaError
from .resource import create_resource, prepare_resource


class Router(CompiledRouter):
    def __init__(self, *, url_prefix: Optional[str] = None):
        self.url_prefix = url_prefix
        self.children: List[Router] = []
        self._uri_mapping: List[str] = []
        super().__init__()

    def route(self, path: str, methods: List[str] = ["get", "head"]):
        def decorated(func):
            self.add_route(path, func, methods=methods)
            return func

        return decorated

    head = partialmethod(route, methods=["head"])
    get = partialmethod(route, methods=["get"])
    post = partialmethod(route, methods=["post"])
    put = partialmethod(route, methods=["put"])
    delete = partialmethod(route, methods=["delete"])
    options = partialmethod(route, methods=["options"])
    patch = partialmethod(route, methods=["patch"])
    trace = partialmethod(route, methods=["trace"])

    def add_route(
        self,
        uri_template: str,
        resource: Union[object, Callable],
        *,
        methods: List[str] = [],
        **kwargs,
    ):
        if methods:
            if not callable(resource):
                raise TypeError(f"resource {resource!r} must be function type")

            resource = create_resource(methods, resource)()

        if self.url_prefix:
            uri_template = self.url_prefix + uri_template

        self._check_endpoint(uri_template)
        self._uri_mapping.append(uri_template)
        prepare_resource(resource)
        super().add_route(uri_template, resource, **kwargs)

    def _check_endpoint(self, uri_template: str):
        if uri_template in self._uri_mapping:
            raise EndpointConflict(f"Endpoint {uri_template!r} already exists")

        for r in self.children:
            r._check_endpoint(uri_template)

    def include_router(self, router: Union["Router", "AsyncRouter"]):
        if not router.url_prefix:
            raise BadRouter("URL prefix needed for nesting router")

        if self.url_prefix:
            raise FalcaError("For now you can only add one router :)")

        self._check_router(router)
        self.children.append(router)

    def _check_router(self, router: Union["Router", "AsyncRouter"]):
        if self.url_prefix and self.url_prefix == router.url_prefix:
            raise EndpointConflict("Router already exists")

        for r in self.children:
            for uri in self._uri_mapping:
                r._check_endpoint(uri)
            r._check_router(router)

    def find(self, uri: str, req=None):
        resource = super().find(uri, req=req)
        if resource is None:
            for router in self.children:
                resource = router.find(uri, req=req)
                if resource:
                    break
        return resource


class AsyncRouter(Router):
    def add_route(
        self,
        uri_template: str,
        resource: Union[object, Callable],
        *,
        methods: List[str] = [],
        **kwargs,
    ):
        kwargs["methods"] = methods
        kwargs["_asgi"] = True
        super().add_route(uri_template, resource, **kwargs)

    websocket = partialmethod(Router.route, methods=["websocket"])
