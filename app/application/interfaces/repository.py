import abc

from app.domain.entity import Domain


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, domain: Domain):
        ...

    @abc.abstractmethod
    def read(self, domain: Domain):
        ...
