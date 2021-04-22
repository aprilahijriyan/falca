from falcon.constants import MEDIA_JSON

from .base import Middleware


class JsonParserMiddleware(Middleware):
    def process_request(self, req, resp):
        if req.content_type != MEDIA_JSON:
            return

        req.json = req.get_media()
