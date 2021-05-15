import falcon

from . import actions


def prepare_resource(klass: object):
    for name in dir(klass):
        method = name[3:].split("_", 1)[0].upper()
        if name.startswith("on_") and method in falcon.COMBINED_METHODS:
            func = getattr(klass, name)
            view = actions.flavor(func)
            setattr(klass, name, view)


class ResourceMeta(type):
    def __call__(cls, *args, **kwds):
        instance = cls.__new__(cls)
        instance.__init__(*args, **kwds)
        prepare_resource(instance)
        return instance


class Resource(metaclass=ResourceMeta):
    pass
