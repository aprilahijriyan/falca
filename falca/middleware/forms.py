from falcon import MEDIA_URLENCODED
from falcon.request import Request
from falcon.response import Response

from .base import Middleware


class FormParserMiddleware(Middleware):
    content_type = MEDIA_URLENCODED

    def process_request(self, req: Request, resp: Response):
        media = {}
        if self.is_valid_content_type(req):
            media = req.get_media()

        req.forms = media
