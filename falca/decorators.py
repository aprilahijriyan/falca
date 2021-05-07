from typing import Union


def use_plugins(plugins: Union[list, tuple]):
    def decorated(obj: object):
        obj.__plugins__ = plugins
        return obj

    return decorated
