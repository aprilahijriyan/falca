from abc import ABCMeta, abstractmethod

from falcon.request import Request

from .schema import Schema


class Annotation(metaclass=ABCMeta):
    def __init__(self, schema: Schema) -> None:
        self.schema = schema
        self.data = {}

    @abstractmethod
    def load(self, request: Request):
        """
        Load data from the request object

        Args:
            request (falcon.request.Request): request object
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
    def load(self, request: Request):
        json = request.json
        self.data = self.validate(json)


class Query(Validator):
    def load(self, request: Request):
        query = request.params
        self.data = self.validate(query)


class Header(Validator):
    def load(self, request: Request):
        headers = request.headers
        self.data = self.validate(headers)


class Form(Validator):
    def load(self, request: Request):
        forms = request.forms
        self.data = self.validate(forms)


class File(Validator):
    def load(self, request: Request):
        files = request.files
        self.data = self.validate(files)
