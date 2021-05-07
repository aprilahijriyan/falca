from abc import ABCMeta, abstractmethod

from falcon.request import Request


class Annotation(metaclass=ABCMeta):
    def __init__(self, schema) -> None:
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


class Query(Annotation):
    def load(self, request: Request):
        query = request.params
        self.data = self.validate(query)

    def validate(self, data: dict):
        pass


class Header(Annotation):
    def load(self, request: Request):
        headers = request.headers
        self.data = self.validate(headers)

    def validate(self, data: dict):
        return super().validate(data)


class Form(Annotation):
    def load(self, request: Request):
        forms = request.forms
        self.data = self.validate(forms)

    def validate(self, data: dict):
        return super().validate(data)


class File(Annotation):
    def load(self, request: Request):
        files = request.files
        self.data = self.validate(files)

    def validate(self, data: dict):
        return super().validate(data)
