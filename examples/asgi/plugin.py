import logging
from typing import Union

from falca.app import ASGI, WSGI
from falca.plugins.base import BasePlugin


class Logger(BasePlugin):
    name = "logging"

    def __init__(self, app: Union[WSGI, ASGI]) -> None:
        super().__init__(app)
        logging.basicConfig(level=logging.INFO)
        self._log = logging.getLogger(app.import_name)

    def info(self, *args, **kwds):
        self._log.info(*args, **kwds)

    def error(self, *args, **kwds):
        self._log.error(*args, **kwds)

    def warning(self, *args, **kwds):
        self._log.warning(*args, **kwds)

    def exception(self, *args, **kwds):
        self._log.exception(*args, **kwds)

    def debug(self, *args, **kwds):
        self._log.debug(*args, **kwds)
