from falcon.asgi.request import Request as ASGIRequest
from falcon.asgi.response import Response as ASGIResponse
from falcon.constants import MEDIA_JSON
from falcon.request import Request
from falcon.response import Response

from .base import Middleware


class JsonParserMiddleware(Middleware):
    content_type = MEDIA_JSON

    def process_request(self, req: Request, resp: Response):
        media = {}
        if self.is_valid_content_type(req) and req.content_length not in (None, 0):
            media = req.get_media()

        req.json = media

    async def process_request_async(self, req: ASGIRequest, resp: ASGIResponse):
        media = {}
        if self.is_valid_content_type(req) and req.content_length not in (None, 0):
            media = await req.get_media()

        req.json = media
