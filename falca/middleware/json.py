from falcon.constants import MEDIA_JSON
from falcon.request import Request
from falcon.response import Response

from .base import Middleware


class JsonParserMiddleware(Middleware):
    def process_request(self, req: Request, resp: Response):
        media = {}
        if req.content_type == MEDIA_JSON and req.content_length not in (None, 0):
            media = req.get_media()
        req.json = media
