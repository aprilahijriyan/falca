import falcon

from . import actions


class ResourceMeta(type):
    def __new__(cls, name, bases, attrs):
        for name, func in attrs.items():
            method = name[3:].split("_", 1)[0].upper()
            if name.startswith("on_") and method in falcon.COMBINED_METHODS:
                view = falcon.before(actions.before)(func)
                attrs[name] = view

        klass = type(name, bases, attrs)
        return klass


class Resource(metaclass=ResourceMeta):
    def render_template(self, template, **kwds):
        t = self.template_lookup.get_template(template)
        return t.render(**kwds)
