from typing import Any, Union

from falcon.asgi.response import Response as _ASGIResponse
from falcon.constants import MEDIA_HTML, MEDIA_JSON
from falcon.response import Response as _Response
from falcon.util.misc import code_to_http_status

from .request import ASGIRequest, Request


class Response:
    content_type: str = None

    def __init__(
        self,
        content: Any,
        status: Union[str, int] = 200,
        content_type: str = None,
        headers: dict = {},
    ) -> None:
        self.content = content
        self.status = status
        self.content_type = content_type or self.content_type
        self.headers = headers
        self._cookies = []
        self._unset_cookies = []

    def set_cookie(self, name, value, **kwds):
        self._cookies.append((name, value, kwds))

    def unset_cookie(self, name, **kwds):
        self._unset_cookies.append((name, kwds))

    def build_content(
        self, req: Union[Request, ASGIRequest], resp: Union[_Response, _ASGIResponse]
    ):
        app = req.context.app
        media_handlers = app.media_handlers
        if self.content_type in media_handlers:
            resp.media = self.content
        else:
            resp.text = self.content

    def build(
        self, req: Union[Request, ASGIRequest], resp: Union[_Response, _ASGIResponse]
    ):
        self.build_content(req, resp)
        resp.content_type = self.content_type
        if isinstance(self.status, int):
            self.status = code_to_http_status(self.status)

        resp.status = self.status
        resp.headers.update(self.headers)
        for name, value, kwds in self._cookies:
            resp.set_cookie(name, value, **kwds)

        for name, kwds in self._unset_cookies:
            resp.unset_cookie(name, **kwds)


class HtmlResponse(Response):
    content_type = MEDIA_HTML

    def __init__(self, content: str, context: dict, **kwds) -> None:
        self.context = context
        super().__init__(content, **kwds)

    def render(self, req: Union[Request, ASGIRequest]):
        t = req.context.templates.get_template(self.content)
        html = t.render(**self.context)
        return html

    def build(
        self, req: Union[Request, ASGIRequest], resp: Union[_Response, _ASGIResponse]
    ):
        self.content = self.render(req)
        super().build(req, resp)


class JsonResponse(Response):
    content_type = MEDIA_JSON

    def __init__(self, content: Union[dict, list], **kwds) -> None:
        super().__init__(content, **kwds)
