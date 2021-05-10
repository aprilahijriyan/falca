from falcon import MEDIA_URLENCODED
from falcon.request import Request
from falcon.response import Response

from .base import Middleware


class FormParserMiddleware(Middleware):
    def process_request(self, req: Request, resp: Response):
        media = {}
        if req.content_type == MEDIA_URLENCODED:
            media = req.media
        req.forms = media
