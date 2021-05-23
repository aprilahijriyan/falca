import inspect
import os
import pkgutil
import sys
from importlib import import_module
from typing import Callable, Dict, Union

import falcon

from .depends import Depends


def abort(code: int, **kwagrs):
    status = falcon.code_to_http_status(code)
    raise falcon.HTTPError(status, **kwagrs)


def import_attr(module: str):
    """
    Functions to get attributes in modules.
    :param module: e.g. os.path
    """

    pkg, name = module.rsplit(".", 1)
    mod = import_module(pkg)
    return getattr(mod, name)


def get_root_path(import_name: str):
    """
    This is taken from https://github.com/pallets/flask/blob/master/src/flask/scaffold.py#L699
    """

    # Module already imported and has a file attribute. Use that first.
    mod = sys.modules.get(import_name)

    if mod is not None and hasattr(mod, "__file__"):
        return os.path.dirname(os.path.abspath(mod.__file__))

    # Next attempt: check the loader.
    loader = pkgutil.get_loader(import_name)

    # Loader does not exist or we're referring to an unloaded main
    # module or a main module without path (interactive sessions), go
    # with the current working directory.
    if loader is None or import_name == "__main__":
        return os.getcwd()

    if hasattr(loader, "get_filename"):
        filepath = loader.get_filename(import_name)
    else:
        # Fall back to imports.
        __import__(import_name)
        mod = sys.modules[import_name]
        filepath = getattr(mod, "__file__", None)

        # If we don't have a file path it might be because it is a
        # namespace package. In this case pick the root path from the
        # first module that is contained in the package.
        if filepath is None:
            raise RuntimeError(
                "No root path can be found for the provided module"
                f" {import_name!r}. This can happen because the module"
                " came from an import hook that does not provide file"
                " name information or because it's a namespace package."
                " In this case the root path needs to be explicitly"
                " provided."
            )

    # filepath is import_name.py for a module, or __init__.py for a package.
    return os.path.dirname(os.path.abspath(filepath))


def get_argnotations(func: Callable) -> Dict[str, type]:
    sig = inspect.signature(func)
    params = {}
    for p in sig.parameters.values():
        name = p.name
        if name == "self":
            continue

        atype = p.annotation
        default = p.default
        if isinstance(default, Depends):
            atype = default

        if atype is inspect._empty:
            continue

        params[name] = atype

    return params


def get_http_description(status_or_code: Union[str, int]):
    status = status_or_code
    if isinstance(status, int):
        status: str = falcon.code_to_http_status(status)

    return status.split(" ", 1)[1]
