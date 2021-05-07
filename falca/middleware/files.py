from typing import List, TextIO

from falcon import MEDIA_MULTIPART
from falcon.media.multipart import BodyPart

from .base import Middleware


class FileStorage:
    def __init__(self, media, filename, name, content_type, headers) -> None:
        self.media = media
        self.filename = filename
        self.name = name
        self.content_type = content_type
        self.headers = headers

    def read(self, size=-1):
        return self.media.stream.read(size)

    def save(self, dst: TextIO, size: int = 16384):
        data = self.read(size)
        dst.write(data)


class FileParserMiddleware(Middleware):
    def process_request(self, req, resp):
        files = {}
        if req.content_type == MEDIA_MULTIPART:
            form: List[BodyPart] = req.get_media()
            for part in form:
                if part.content_type == MEDIA_MULTIPART:
                    media = part.get_media()
                    name = part.name
                    storage = FileStorage(
                        media,
                        part.secure_filename,
                        name,
                        part.content_type,
                        part._headers,
                    )
                    data = files.get(name, [])
                    data.append(storage)
                    files[name] = data

        req.files = files
