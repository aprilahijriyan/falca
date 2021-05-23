from functools import update_wrapper
from inspect import Parameter, signature
from typing import Any, Callable, Optional


class Depends:
    def __init__(self, handler: Optional[Callable[..., Any]] = None) -> None:
        self.handler = handler
        if callable(self.handler):
            update_wrapper(type(self).__call__, handler)
            oldsig = signature(handler)
            params = list(oldsig.parameters.values())
            for param in params:
                assert (
                    param.name != "self"
                ), "You cannot add the 'self' parameter to the 'handler'"

            params.insert(0, Parameter("self", Parameter.POSITIONAL_ONLY))
            newsig = oldsig.replace(parameters=params)
            type(self).__call__.__signature__ = newsig

    def __call__(self, *args, **kwds):
        assert callable(self.handler), "The handler must be a callable object"
        return self.handler(*args, **kwds)
