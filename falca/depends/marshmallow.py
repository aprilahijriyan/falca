from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Optional, Union

from six import with_metaclass

from ..request import ASGIRequest, Request
from ..serializers.marshmallow import DefaultSchemaMeta, Schema
from .base import Depends


class Marshmallow(with_metaclass(ABCMeta, Depends)):
    def __init__(self, schema: Optional[Union[Schema, Dict[str, Any]]] = None) -> None:
        if isinstance(schema, dict):
            schema = Schema.from_dict(schema)()
        elif type(schema) is DefaultSchemaMeta:
            schema = schema()
        elif isinstance(schema, Schema) or schema is None:
            pass
        else:  # pragma: no cover
            raise TypeError(f"schema type must be of type {Schema!r} or dict")

        self.schema: Schema = schema

    @abstractmethod
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        pass

    def validate(self, request: Union[Request, ASGIRequest]):
        data = self.get_data(request)
        if self.schema is not None:
            data = self.schema.load(data)
        return data

    def __call__(self, request: Union[Request, ASGIRequest]) -> dict:
        data = self.validate(request)
        return data


class Query(Marshmallow):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.params


class Form(Marshmallow):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.forms


class File(Marshmallow):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.files


class Body(Marshmallow):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.json


class Header(Marshmallow):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.headers


class Cookie(Marshmallow):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.cookies
