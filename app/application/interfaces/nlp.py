import abc
from typing import List

from app.domain.entity import MrcDomain, QueryDomain


class AbstractNLP(abc.ABC):
    @abc.abstractmethod
    def predict(self, domain: MrcDomain):
        ...

    @abc.abstractmethod
    def get_embeddings(self, domain: QueryDomain) -> List:
        ...

    @abc.abstractmethod
    def get_nouns_verbs(self, domain: QueryDomain) -> (List, List):
        ...

    @abc.abstractmethod
    def get_pos(self, domain: QueryDomain) -> List:
        ...