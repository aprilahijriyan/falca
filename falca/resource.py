from typing import Any, Union

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
    request: falcon.Request = None
    response: falcon.Response = None

    def make_response(
        self, data: Any, content_type, *, status=falcon.HTTP_200, headers={}
    ):
        app = self.request.context.app
        media_handlers = app.media_handlers
        if content_type in media_handlers:
            self.response.media = data
        else:
            self.response.text = data

        self.response.content_type = content_type
        self.response.status = status
        self.response.headers.update(headers)

    def json(self, payload: Union[dict, list], **kwds):
        self.make_response(payload, falcon.MEDIA_JSON, **kwds)

    def html(self, template: str, context={}, **kwds):
        html = self.render(template, **context)
        self.make_response(html, falcon.MEDIA_HTML, **kwds)

    def render(self, template: str, **kwds):
        t = self.request.context.templates.get_template(template)
        html = t.render(**kwds)
        return html
