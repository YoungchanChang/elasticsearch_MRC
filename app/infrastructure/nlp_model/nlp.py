import re
import numpy as np

from app.application.interfaces.nlp import AbstractNLP
from app.application.service.elastic_service import ElasticService
from app.controller.elastic_controller import ElasticParsingResult
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

    # def get_elastic_content(self, question: str):
    #     content_repository = el_repo.ElasticContent()
    #     title_repository = el_repo.ElasticTitle()
    #     elastic_service = ElasticService(title_repository, content_repository)
    #
    #     elastic_content = elastic_service.get_content(question)
    #
    #     return filtered_elastic_content

BEST_VALUE = 0
MRC_ANSWER = 0
MRC_INDEX = 1
MRC_NOT_FOUND = ''
END_IDX = 1

SENTENCE_SPLIT_SYMBOL = "@"

class ElasticMrc:

    def __init__(self):
        self.es_repo = es_repo.ElasticRepository()
        self.nlp_model = PororoMecab()
        self.es_service = ElasticService(elastic=self.es_repo, nlp_model=self.nlp_model)

    def put_mrc_content(self, question: str):
        result = self.es_service.insert_data(sentence=question)
        return result

    def get_content(self, question: str):
        elastic_content = self.es_service.search(sentence=question)
        return elastic_content

    def extract_elastic_data(self, elastic_item: dict):
        _score = elastic_item['_score']
        _source = elastic_item['_source']
        title, first_header, second_header, content = _source['title'], _source['first_header'], _source[
            'second_header'], _source['content']
        detail_items = elastic_item['_explanation']['details'][0]['details'][0]['details']

        noun_matches = []
        verb_matches = []
        content_match = []
        for detail_item in detail_items:
            if "content_noun_search" in detail_item['description']:
                matching_noun = re.findall("content_noun_search:([가-힣|\w]+)", str(detail_item['description']))
                noun_matches.extend(matching_noun)
            elif "content_verb_search" in detail_item['description']:
                matching_noun = re.findall("content_verb_search:([가-힣|\w]+)", str(detail_item['description']))
                noun_matches.extend(matching_noun)
            else:
                content_matches = list(set(re.findall("content:([가-힣|\w]+)", str(detail_item['description']))))
                content_match.extend(content_matches)
        elastic_parsing_result = ElasticParsingResult(score=_score, title=title, first_header=first_header, second_header=second_header, content=content, content_noun_tokens=noun_matches, content_verb_tokens=verb_matches, content_match_tokens=content_match)
        return elastic_parsing_result

    def get_mrc_content(self, question: str, elastic_contents: List):

        elastic_contents = [self.extract_elastic_data(x) for x in elastic_contents]

        mrc_cand_list = []
        for idx, items in enumerate(elastic_contents):
            symbol_idx = ""
            if len(elastic_contents) != (idx+1):
                symbol_idx = SENTENCE_SPLIT_SYMBOL*(idx+1)
            mrc_item = items.content + " " + symbol_idx + " "
            item_length = len(mrc_item)
            mrc_cand_list.append((mrc_item, items.content, item_length))

        mrc_candidates = [x[BEST_VALUE] for x in mrc_cand_list]
        mrc_sentence = f"".join(mrc_candidates)
        mrc_domain = MrcDomain(question, mrc_sentence)
        mrc_answer = self.nlp_model.predict(domain=mrc_domain)

        mrc_hit_words = mrc_answer[MRC_ANSWER]

        if mrc_hit_words == MRC_NOT_FOUND:
            return "NotHit", elastic_contents[BEST_VALUE].content, elastic_contents[BEST_VALUE]

        total_length = 0
        end_pos = mrc_answer[MRC_INDEX][END_IDX]
        mrc_answer = ''
        elastic_hit_idx = 0
        for idx, mrc_cand_item in enumerate(mrc_cand_list):
            total_length += mrc_cand_item[2]
            if end_pos < total_length:
                mrc_answer = mrc_cand_item[1]
                elastic_hit_idx = idx
                break

        return mrc_hit_words, mrc_answer, elastic_contents[elastic_hit_idx]


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