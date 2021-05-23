try:
    from marshmallow import Schema as BaseSchema
    from marshmallow.schema import SchemaMeta

except ImportError:
    raise ImportError(
        "You need to install the 'marshmallow' module if you want to use 'falca.serializers.marshmallow'"
    )

from six import with_metaclass

from ..compat import json


class SchemaConfig:
    render_module = json


class DefaultSchemaMeta(SchemaMeta):
    def __call__(cls, *args, **kwds):
        config = getattr(cls, "Meta", None)
        if config:
            config.render_module = json
        else:
            setattr(cls, "Meta", SchemaConfig)

        instance = cls.__new__(cls)
        instance.__init__(*args, **kwds)
        return instance


class Schema(with_metaclass(DefaultSchemaMeta, BaseSchema)):
    pass
