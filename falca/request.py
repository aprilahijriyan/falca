from typing import Any, Dict

from falcon.asgi.request import Request as _ASGIRequest
from falcon.request import Request as _Request


class RequestMixin:
    json: Dict[str, Any] = {}
    forms: Dict[str, Any] = {}
    files: Dict[str, Any] = {}


class Request(_Request, RequestMixin):
    pass


class ASGIRequest(_ASGIRequest, RequestMixin):
    pass
