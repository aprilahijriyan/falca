from typing import Union

from ..request import ASGIRequest, Request
from .base import Depends


class Plugin(Depends):
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, *args, request: Union[Request, ASGIRequest] = None):
        app = request.context.app
        return app.plugins.get(self.name)
