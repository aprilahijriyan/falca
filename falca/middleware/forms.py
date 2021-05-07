from falcon import MEDIA_URLENCODED

from .base import Middleware


class FormParserMiddleware(Middleware):
    def process_request(self, req, resp):
        media = {}
        if req.content_type == MEDIA_URLENCODED:
            media = req.media
        req.forms = media
