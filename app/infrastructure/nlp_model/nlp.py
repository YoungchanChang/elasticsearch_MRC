import re
import numpy as np

from app.application.interfaces.nlp import AbstractNLP
from app.application.service.elastic_service import ElasticService
from app.domain.entity import MrcDomain
from pororo import Pororo

from app.infrastructure.database.elastic_repository import ElasticRepository
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

    # def get_elastic_content(self, question: str):
    #     content_repository = el_repo.ElasticContent()
    #     title_repository = el_repo.ElasticTitle()
    #     elastic_service = ElasticService(title_repository, content_repository)
    #
    #     elastic_content = elastic_service.get_content(question)
    #
    #     return filtered_elastic_content

MRC_TOKEN_VECTOR_SENTENCE_LIMIT = 2
MRC_TOKEN_KEYWORD_SENTENCE_LIMIT = 3

KEYWORD_LENGTH = 1
VECTOR_LENGTH = 2
BEST_VALUE = 0
MRC_ANSWER = 0
MRC_INDEX = 1
MRC_NOT_FOUND = ''
ONLY_ONE_CONTENT = 0
START_IDX = 0
END_IDX = 0

SENTENCE_SPLIT_SYMBOL = " @@@ "

class ElasticMrc:

    def __init__(self):
        self.es_repo = ElasticRepository()
        self.nlp_model = PororoMecab()
        self.es_service = ElasticService(elastic=self.es_repo, nlp_model=self.nlp_model)

    def put_mrc_content(self, question: str):
        result = self.es_service.insert_data(sentence=question)
        return result

    def get_mrc_content(self, question: str):
        elastic_content = self.es_service.search(sentence=question)
        title = elastic_content[BEST_VALUE]["title"]
        elastic_content = [x["content"] for x in elastic_content]

        mrc_sentence = f"{SENTENCE_SPLIT_SYMBOL}".join(elastic_content)
        mrc_domain = MrcDomain("test", "test")
        mrc_answer = self.nlp_model.predict(mrc_domain)

        split_index_data = [(m.start(), m.end()) for m in re.finditer(SENTENCE_SPLIT_SYMBOL, mrc_sentence)]

        best_proper_content = elastic_content[BEST_VALUE]


        if (len(split_index_data) > ONLY_ONE_CONTENT) and (mrc_answer[MRC_ANSWER] != MRC_NOT_FOUND):

            tmp_answer = []
            for i in mrc_sentence.split(SENTENCE_SPLIT_SYMBOL):
                if len(mrc_answer[0]) >= 1 and mrc_answer[0] in i:
                    best_proper_content = i
                    tmp_answer.append(i)

            if len(tmp_answer) > 2:
                start_idx = 0
                save_idx = None
                for idx, split_item in enumerate(split_index_data):
                    if mrc_answer[MRC_INDEX][START_IDX] > start_idx and mrc_answer[MRC_INDEX][START_IDX] < split_item[START_IDX]:
                        save_idx = idx
                        break
                    start_idx = split_item[START_IDX]

                    if mrc_answer[MRC_INDEX][START_IDX] >= split_item[START_IDX]:
                        save_idx = idx + 1

                best_proper_content = mrc_sentence.split(SENTENCE_SPLIT_SYMBOL)[save_idx]

                if save_idx is None:
                    best_proper_content = elastic_content[BEST_VALUE]

        return mrc_answer[MRC_ANSWER], best_proper_content, title


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