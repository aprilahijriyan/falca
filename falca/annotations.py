from abc import ABCMeta, abstractmethod
from typing import Union

from .request import ASGIRequest, Request
from .schema import Schema


class Annotation(metaclass=ABCMeta):
    def __init__(self, schema: Schema) -> None:
        self.schema = schema
        self.data = {}

    @abstractmethod
    def load(self, request: Union[Request, ASGIRequest]):
        """
        Load data from the request object

        Args:
            request (Union[falca.request.Request, falca.request.ASGIRequest]): request object
        """

    @abstractmethod
    def validate(self, data: dict):
        """
        data validation here

        Args:
            data (dict): Can be (params, headers, files)
        """


class Validator(Annotation):
    def validate(self, data: dict):
        return self.schema.load(data)


class Body(Validator):
    def load(self, request: Union[Request, ASGIRequest]):
        json = request.json
        self.data = self.validate(json)


class Query(Validator):
    def load(self, request: Union[Request, ASGIRequest]):
        query = request.params
        self.data = self.validate(query)


class Header(Validator):
    def load(self, request: Union[Request, ASGIRequest]):
        headers = request.headers
        self.data = self.validate(headers)


class Form(Validator):
    def load(self, request: Union[Request, ASGIRequest]):
        forms = request.forms
        self.data = self.validate(forms)


class File(Validator):
    def load(self, request: Union[Request, ASGIRequest]):
        files = request.files
        self.data = self.validate(files)
