
import numpy as np

from app.application.interfaces.nlp import AbstractNLP
from app.application.service.keyword_vector_repository import KeywordVectorRepository
from app.controller.elastic_controller import ElasticParsingResult, parse_elastic_data, ElasticMrcController
from app.domain.entity import MrcDomain
from pororo import Pororo

import app.infrastructure.database.elastic_repository as es_repo
from app.infrastructure.nlp_model.mecab_model import *

se = Pororo(task="sentence_embedding", lang="ko")
mrc = Pororo(task="mrc", lang="ko")


class PororoMecab(AbstractNLP):
    def predict(self, domain: MrcDomain):
        mrc_answer = mrc(
            domain.query,
            domain.search_string
        )
        return mrc_answer

    def get_embeddings(self, domain: QueryDomain) -> List:
        se_val = se(" ".join(domain.query))
        return np.array(se_val).tolist()

    def get_nouns_verbs(self, domain: QueryDomain) -> (List, List):
        mecab_tokens = list(MecabInflectParser(domain.query).gen_mecab_compound_token_feature())
        mecab_noun_tokens = [x[MECAB_WORD] for x in mecab_tokens if x[MECAB_POS] == NOUN]
        mecab_verb_tokens = [x[MECAB_WORD] for x in mecab_tokens if x[MECAB_POS] == VERB]
        return mecab_noun_tokens, mecab_verb_tokens

    def get_pos(self, domain: QueryDomain) -> List:
        mecab_parsed = mecab.parse(domain.query)
        return [(x[0], x[1].pos) for x in mecab_parsed]


class ElasticMrc(ElasticMrcController):

    def __init__(self):
        super().__init__(nlp_model=PororoMecab())
        self.es_repo = es_repo.ElasticRepository()
        self.es_service = KeywordVectorRepository(repository=self.es_repo, nlp_model=self.nlp_model)

    def put_mrc_content(self, question: str):
        result = self.es_service.create(query=question)
        return result

    def get_content(self, question: str):
        elastic_content = self.es_service.read(query=question)
        return elastic_content


if __name__ == "__main__":
    d_item = "잡혔었었다."
    for i in list(MecabInflectParser("김보당은 정중부에게 붙잡혔다.").gen_mecab_compound_token_feature()):
        print(i)
    mecab_tokens = list(MecabInflectParser(d_item).gen_mecab_compound_token_feature())
    print(mecab_tokens)
    mecab_noun_tokens = [x[0] for x in mecab_tokens if x[1] == NOUN]
    print(mecab_noun_tokens)
    mecab_verb_tokens = [x[0] for x in mecab_tokens if x[1] == VERB]
    print(mecab_verb_tokens)