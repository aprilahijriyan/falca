from falcon.asgi.request import Request as _ASGIRequest
from falcon.request import Request as _Request


class RequestMixin:
    json = {}
    forms = {}
    files = {}


class Request(_Request, RequestMixin):
    pass


class ASGIRequest(_ASGIRequest, RequestMixin):
    pass
