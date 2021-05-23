from typing import Union

from ..request import ASGIRequest, Request
from .base import Depends


class Plugin(Depends):
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, *args, request: Union[Request, ASGIRequest]):
        app = request.context.app
        return app.plugins.get(self.name)


class Settings(Depends):
    def __init__(self, name: str = None) -> None:
        self.name = name

    def __call__(self, *args, request: Union[Request, ASGIRequest]):
        app = request.context.app
        settings = app.settings
        if self.name is not None:
            settings = settings.get(self.name)
        return settings
