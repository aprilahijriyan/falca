from typing import Any

import falcon

from . import actions


class ResourceMeta(type):
    def __new__(cls, name, bases, attrs):
        for name, func in attrs.items():
            method = name[3:].split("_", 1)[0].upper()
            if name.startswith("on_") and method in falcon.COMBINED_METHODS:
                view = falcon.before(actions.before)(actions.flavor(func))
                attrs[name] = view

        print("Resource:", name, attrs)
        klass = type(name, bases, attrs)
        return klass


class Resource(metaclass=ResourceMeta):
    request: falcon.Request = None
    response: falcon.Response = None

    def build_response(
        self, data: Any, content_type, *, status=falcon.HTTP_200, headers={}
    ):
        self.response.content_type = content_type
        self.response.media = data
        self.response.status = status
        self.response.headers.update(headers)

    def json(self, payload, **kwds):
        self.build_response(payload, falcon.MEDIA_JSON, **kwds)

    def html(self, template, context={}, **kwds):
        html = self.render(template, **context)
        self.build_response(html, falcon.MEDIA_HTML, **kwds)

    def render(self, template, **kwds):
        t = self.template_lookup.get_template(template)
        html = t.render(**kwds)
        return html

    # def __call__(self) -> Any:
    #     return self
