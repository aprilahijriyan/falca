from falcon.app import App as WSGIBase
from falcon.asgi import App as ASGIBase

from .scaffold import Scaffold


class WSGI(Scaffold, WSGIBase):
    pass


class ASGI(Scaffold, ASGIBase):
    pass
