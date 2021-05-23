from typing import Any, Dict, Union

from ..request import ASGIRequest, Request
from ..serializers.marshmallow import Schema
from .base import Depends


class Marshmallow(Depends):
    def __init__(self, schema: Union[Schema, Dict[str, Any]]) -> None:
        assert isinstance(
            schema, (Schema, dict)
        ), f"schema type must be of type {Schema!r} or dict"
        if isinstance(schema, dict):
            schema = Schema.from_dict(schema)

        self.schema: Schema = schema


class Query(Marshmallow):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.load(request.params)
        return data


class Form(Marshmallow):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.load(request.forms)
        return data


class File(Marshmallow):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.load(request.files)
        return data


class Body(Marshmallow):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.load(request.json)
        return data


class Header(Marshmallow):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.load(request.headers)
        return data


class Cookie(Marshmallow):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.load(request.cookies)
        return data
