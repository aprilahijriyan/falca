try:
    from pydantic import BaseModel
    from pydantic.main import ModelMetaclass
except ImportError:
    raise ImportError(
        "You need to install the 'pydantic' module if you want to use 'falca.serializers.pydantic'"
    )

from six import with_metaclass

from ..compat import json


class SchemaMeta(ModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):
        klass = super().__new__(mcs, name, bases, namespace, **kwargs)
        config = getattr(klass, "Config")
        config.json_dumps = json.dumps
        config.json_loads = json.loads
        return klass


class Schema(with_metaclass(SchemaMeta, BaseModel)):
    pass
