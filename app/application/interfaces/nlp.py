import abc
from typing import List

from app.domain.entity import Domain


class AbstractNLP(abc.ABC):
    @abc.abstractmethod
    def predict(self, domain: Domain):
        ...

    @abc.abstractmethod
    def get_embeddings(self, domain: Domain) -> List:
        ...

    @abc.abstractmethod
    def get_nouns_verbs(self, domain: Domain) -> (List, List):
        ...

    @abc.abstractmethod
    def get_pos(self, domain: Domain) -> List:
        ...