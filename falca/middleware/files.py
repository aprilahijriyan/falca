from io import BytesIO
from typing import List, TextIO

from falcon import MEDIA_MULTIPART
from falcon.constants import MEDIA_TEXT
from falcon.media.multipart import BodyPart
from falcon.request import Request
from falcon.response import Response

from .base import Middleware


class FileStorage:
    def __init__(
        self, stream: TextIO, filename: str, name: str, content_type: str, headers: dict
    ) -> None:
        self.stream = stream
        self.filename = filename
        self.name = name
        self.content_type = content_type
        self.headers = headers

    def read(self, size: int = None):
        if size:
            return self.stream.read(size)
        return self.stream.read()

    def save(self, dst: TextIO, *, size: int = None):
        data = self.read(size)
        dst.write(data)


class FileParserMiddleware(Middleware):
    content_type = MEDIA_MULTIPART

    def process_request(self, req: Request, resp: Response):
        files = {}
        forms = {}
        if self.is_valid_content_type(req):
            parts: List[BodyPart] = req.get_media()
            for part in parts:
                name = part.name
                if part.content_type in MEDIA_TEXT and part.filename is None:
                    data = forms.get(name)
                    if data and not isinstance(data, list):
                        data = [data]
                    else:
                        data = part.text

                    if isinstance(data, list):
                        data.append(part.text)

                    forms[name] = data
                else:
                    buffer = BytesIO(part.stream.read())
                    storage = FileStorage(
                        buffer,
                        part.secure_filename,
                        name,
                        part.content_type,
                        part._headers,
                    )
                    data = files.get(name)
                    if data and not isinstance(data, list):
                        data = [data]
                    else:
                        data = storage

                    if isinstance(data, list):
                        data.append(storage)

                    files[name] = data

        req.files = files
        req.forms = forms
