import os
from importlib import import_module
from types import ModuleType
from typing import Any, Dict, Union

from .helpers import import_attr


class Settings(dict):
    def from_object(self, src: Union[str, object], **kwds):
        if isinstance(src, str):
            obj = import_attr(src)
        else:
            obj = src

        self.from_dict(vars(obj), **kwds)

    def from_envvar(self, src: str, **kwds):
        cfg = os.environ[src]
        obj = import_module(cfg)
        self.from_dict(vars(obj), **kwds)

    def from_dict(self, src: Dict[str, Any], *, prefix: str = None):
        for k, v in src.items():
            if k.startswith("_") or isinstance(v, ModuleType):
                continue

            if prefix:
                if not k.startswith(prefix):
                    continue

                k = k.lstrip(prefix)

            vv = self.get(k)
            if isinstance(v, dict) and isinstance(vv, dict):
                vv.update(v)
                v = vv

            self[k] = v
