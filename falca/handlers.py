from typing import Union

from falcon.asgi.response import Response as ASGIResponse
from falcon.constants import MEDIA_JSON
from falcon.http_error import HTTPError
from falcon.response import Response
from falcon.status_codes import HTTP_422

from .helpers import get_http_description
from .request import ASGIRequest, Request

try:
    from marshmallow.exceptions import ValidationError as MarshmallowValidationError
except ImportError:
    MarshmallowValidationError = None

try:
    from pydantic.error_wrappers import ValidationError as PydanticValidationError
except ImportError:
    PydanticValidationError = None


def http_handler(
    req: Union[Request, ASGIRequest],
    resp: Union[Response, ASGIResponse],
    exc: HTTPError,
):
    resp.content_type = MEDIA_JSON
    code = exc.code or int(exc.title.split(" ", 1)[0])
    description = exc.description or get_http_description(code)
    resp.media = {
        "status": {"code": code, "description": description},
        "link": exc.link,
    }


if MarshmallowValidationError:

    def marshmallow_handler(
        req: Union[Request, ASGIRequest],
        resp: Union[Response, ASGIResponse],
        exc: MarshmallowValidationError,
        *args,
    ):
        resp.status = HTTP_422
        resp.content_type = MEDIA_JSON
        resp.media = {
            "status": {"code": 422, "description": get_http_description(422)},
            "data": exc.messages,
        }

    async def marshmallow_handler_async(
        req: Union[Request, ASGIRequest],
        resp: Union[Response, ASGIResponse],
        exc: MarshmallowValidationError,
        *args,
    ):
        marshmallow_handler(req, resp, exc, *args)


if PydanticValidationError:

    def pydantic_handler(
        req: Union[Request, ASGIRequest],
        resp: Union[Response, ASGIResponse],
        exc: PydanticValidationError,
        *args,
    ):
        resp.status = HTTP_422
        resp.content_type = MEDIA_JSON
        resp.media = {
            "status": {"code": 422, "description": get_http_description(422)},
            "data": exc.errors(),
        }

    async def pydantic_handler_async(
        req: Union[Request, ASGIRequest],
        resp: Union[Response, ASGIResponse],
        exc: PydanticValidationError,
        *args,
    ):
        pydantic_handler(req, resp, exc, *args)
