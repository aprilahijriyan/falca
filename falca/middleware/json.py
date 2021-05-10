from falcon.constants import MEDIA_JSON

from .base import Middleware


class JsonParserMiddleware(Middleware):
    def process_request(self, req, resp):
        media = {}
        if req.content_type == MEDIA_JSON and req.content_length not in (None, 0):
            media = req.get_media()
        req.json = media
