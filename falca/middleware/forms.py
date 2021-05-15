from falcon import MEDIA_URLENCODED
from falcon.asgi.response import Response as ASGIResponse
from falcon.response import Response

from ..request import ASGIRequest, Request
from .base import Middleware


class FormParserMiddleware(Middleware):
    content_type = MEDIA_URLENCODED

    def process_request(self, req: Request, resp: Response):
        media = {}
        if self.is_valid_content_type(req):
            media = req.get_media()

        req.forms = media

    async def process_request_async(self, req: ASGIRequest, resp: ASGIResponse):
        media = {}
        if self.is_valid_content_type(req):
            media = await req.get_media()

        req.forms = media
