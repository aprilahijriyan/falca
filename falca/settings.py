import os
from importlib import import_module

from .helpers import import_attr


class Settings(dict):
    def from_object(self, src: str):
        obj = import_attr(src)
        self.from_dict(vars(obj))

    def from_envvar(self, src: str):
        cfg = os.environ[src]
        obj = import_module(cfg)
        self.from_dict(vars(obj))

    def from_dict(self, src: dict):
        for k, v in src.items():
            vv = self.get(k)
            if isinstance(v, dict) and isinstance(vv, dict):
                vv.update(v)
                self[k] = vv
            else:
                self[k] = v
