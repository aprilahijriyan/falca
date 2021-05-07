from abc import ABCMeta, abstractmethod


class BaseLoader(metaclass=ABCMeta):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def load(self):
        pass
