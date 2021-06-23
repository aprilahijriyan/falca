from functools import wraps
from mimetypes import guess_type
from typing import Any, AsyncGenerator, Dict, Generator, List, Tuple, Union

from falcon.asgi.response import Response as _ASGIResponse
from falcon.constants import MEDIA_HTML, MEDIA_JSON, MEDIA_TEXT
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
        self._stacked: Dict[str, List[Tuple[Any, Dict[str, Any]]]] = {}

    def _save_args(self, key: str, args: Tuple[Any], kwds: dict):
        try:
            stack = self._stacked[key]
        except KeyError:
            stack = self._stacked[key] = []

        stack.append((args, kwds))

    @wraps(_Response.set_cookie)
    def set_cookie(self, *args, **kwds):
        key = "set_cookie"
        self._save_args(key, args, kwds)

    @wraps(_Response.unset_cookie)
    def unset_cookie(self, *args, **kwds):
        key = "unset_cookie"
        self._save_args(key, args, kwds)

    @wraps(_Response.append_header)
    def append_header(self, *args, **kwds):
        key = "append_header"
        self._save_args(key, args, kwds)

    @wraps(_Response.delete_header)
    def delete_header(self, *args, **kwds):
        key = "delete_header"
        self._save_args(key, args, kwds)

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
        resp.set_headers(self.headers)
        for name, params in self._stacked.items():
            method = getattr(resp, name)
            for args, kwds in params:
                method(*args, **kwds)


class HTMLResponse(Response):
    content_type = MEDIA_HTML

    def __init__(self, content: str, context: dict = {}, **kwds) -> None:
        self.context = context
        super().__init__(content, **kwds)

    def render(self, req: Union[Request, ASGIRequest]):
        t = req.context.templates.get_template(self.content)
        html = t.render(**self.context)
        return html

    def build_content(
        self, req: Union[Request, ASGIRequest], resp: Union[_Response, _ASGIResponse]
    ):
        self.content = self.render(req)
        return super().build_content(req, resp)


class JSONResponse(Response):
    content_type = MEDIA_JSON

    def __init__(self, content: Union[dict, list], **kwds) -> None:
        super().__init__(content, **kwds)


class TextResponse(Response):
    content_type = MEDIA_TEXT

    def __init__(self, content: str, **kwds):
        super().__init__(content, **kwds)


class StreamingResponse(Response):
    def __init__(self, content: Union[AsyncGenerator, Generator], **kwds):
        super().__init__(content, **kwds)

    def build_content(
        self, req: Union[Request, ASGIRequest], resp: Union[_Response, _ASGIResponse]
    ):
        resp.stream = self.content


class FileResponse(StreamingResponse):
    """
    Reference: https://falcon.readthedocs.io/en/stable/user/recipes/output-csv.html
    """

    def __init__(
        self, filename: str, content: Union[str, AsyncGenerator, Generator], **kwds
    ):
        self.filename = filename
        kwds["content_type"] = guess_type(filename)[0]
        super().__init__(content, **kwds)

    def build_content(
        self, req: Union[Request, ASGIRequest], resp: Union[_Response, _ASGIResponse]
    ):
        resp.downloadable_as = self.filename
        if isinstance(self.content, str):
            resp.text = self.content
        else:
            resp.stream = self.content


class StreamingVideoResponse(StreamingResponse):
    """
    Taken from https://stackoverflow.com/questions/53595351/how-to-stream-video-motion-jpeg-using-falcon-server
    """

    content_type = "multipart/x-mixed-replace; boundary=frame"
