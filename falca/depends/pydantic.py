from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from six import with_metaclass

from ..request import ASGIRequest, Request
from ..serializers.pydantic import Schema
from .base import Depends


class Pydantic(with_metaclass(ABCMeta, Depends)):
    def __init__(self, schema: Optional[Schema] = None):
        assert schema is None or issubclass(
            schema, Schema
        ), f"schema type must be of type {Schema!r}"
        self.schema = schema

    @abstractmethod
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        pass

    def validate(self, request: Union[Request, ASGIRequest]):
        data = self.get_data(request)
        if self.schema is not None:
            data = self.schema.parse_obj(data).dict()
        return data

    def __call__(self, request: Union[Request, ASGIRequest]) -> dict:
        data = self.validate(request)
        return data


class Query(Pydantic):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.params


class Form(Pydantic):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.forms


class File(Pydantic):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.files


class Body(Pydantic):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.json


class Header(Pydantic):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.headers


class Cookie(Pydantic):
    def get_data(self, request: Union[Request, ASGIRequest]) -> dict:
        return request.cookies
