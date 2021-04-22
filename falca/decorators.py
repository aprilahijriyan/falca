def use_plugins(plugins):
    def decorated(obj: object):
        obj.__plugins__ = plugins
        return obj

    return decorated


def authenticate(roles=[]):
    pass
