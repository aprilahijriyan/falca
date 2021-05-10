from functools import wraps
from typing import Callable

from .annotations import Annotation
from .helpers import get_argnotations, get_plugins


def flavor(func: Callable):
    @wraps(func)
    def decorated(*args, **kwargs):
        req_object = args[0]
        plugins = get_plugins(req_object, func)
        kwargs.update(plugins)
        args = args[2:]  # without req, resp
        params = get_argnotations(func)
        for key, atype in params.items():
            if isinstance(atype, Annotation):
                atype.load(req_object)
                kwargs[key] = atype

        func(*args, **kwargs)

    return decorated
