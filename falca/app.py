from falcon.app import App as WSGIBase
from falcon.asgi import App as ASGIBase

from .scaffold import Scaffold


class WSGI(WSGIBase, Scaffold):
    def __init__(self, import_name: str, **kwds):
        super().__init__(**kwds)
        Scaffold.__init__(self, import_name, **kwds)


class ASGI(ASGIBase, Scaffold):
    def __init__(self, import_name: str, **kwds):
        super().__init__(**kwds)
        Scaffold.__init__(self, import_name, **kwds)
