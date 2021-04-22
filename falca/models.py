from marshmallow import Schema as BaseSchema
from six import with_metaclass

from .compat import json


class SchemaConfig:
    render_module = json


class DefaultMetaSchema(type):
    def __new__(cls, name, bases, attrs):
        config = attrs.get("Meta")
        if config:
            config.render_module = json
        else:
            config = SchemaConfig

        attrs["Meta"] = config
        klass = type(name, bases, attrs)
        return klass


class Schema(with_metaclass(DefaultMetaSchema, BaseSchema)):
    pass
