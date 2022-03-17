import abc

from app.domain.domain import Domain


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, model: Domain):
        ...

    @abc.abstractmethod
    def find_one(self, model: Domain):
        ...
