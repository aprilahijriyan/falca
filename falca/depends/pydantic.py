from typing import Union

from ..request import ASGIRequest, Request
from ..serializers.pydantic import Schema
from .base import Depends


class Pydantic(Depends):
    def __init__(self, schema: Schema):
        assert issubclass(schema, Schema), f"schema type must be of type {Schema!r}"
        self.schema = schema


class Query(Pydantic):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.parse_obj(request.params)
        return data.dict()


class Form(Pydantic):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.parse_obj(request.forms)
        return data.dict()


class File(Pydantic):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.parse_obj(request.files)
        return data.dict()


class Body(Pydantic):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.parse_obj(request.json)
        return data.dict()


class Header(Pydantic):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.parse_obj(request.headers)
        return data.dict()


class Cookie(Pydantic):
    def __call__(self, *args, request: Union[Request, ASGIRequest]) -> dict:
        data = self.schema.parse_obj(request.cookies)
        return data.dict()
