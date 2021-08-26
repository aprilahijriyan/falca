from abc import ABCMeta, abstractmethod

from mako.lookup import TemplateLookup
from six import with_metaclass


class TemplateEngine(with_metaclass(ABCMeta)):
    @abstractmethod
    def get_template(self, template: str):
        pass


class MakoTemplate(TemplateEngine):
    def __init__(self, *args, **kwds) -> None:
        self.engine = TemplateLookup(*args, **kwds)

    def get_template(self, template: str):
        return self.engine.get_template(template)
