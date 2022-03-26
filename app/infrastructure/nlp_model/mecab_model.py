from typing import Generator, List
import mecab
from python_mecab_ner.mecab_parser import MecabParser

from app.domain.entity import QueryDomain

mecab = mecab.MeCab()
NOUN = "Noun"
VERB = "Verb"

mecab_pos_allow = ["NNG", "NNP", "NR",
                    "VV", "VA", "VX",
                    "XPN", "XR",
                    "MM",
                    "SL", "SH", "SN",]

mecab_noun_pos = ["NNG", "NNP",
                  "MM",
                  "XR",
                  "SL", "SH", "SN",
                  "UNKOWN"]

mecab_verb_pos = ["VV", "VA"]


stop_words = ['하']

MECAB_WORD = 0
MECAB_POS = 1


def get_least_meaning(domain: QueryDomain) -> List:
    mecab_tokens = list(MecabInflectParser(domain.query).gen_mecab_compound_token_feature())
    mecab_least_meaning = [x[MECAB_WORD] for x in mecab_tokens]
    return mecab_least_meaning


class MecabInflectParser(MecabParser):

    type_list = ["Inflect"]

    def tokenize_mecab_compound(self) -> Generator:

        """
        메캅으로 분석한 토큰 제너레이터로 반환 결과 중에 복합여, 굴절형태소 있는 경우 토큰화
        """

        for compound_include_item in self.gen_mecab_token_feature():
            if compound_include_item.type in self.type_list:
                compound_item_list = compound_include_item.expression.split("+")
                for compound_item in compound_item_list:
                    word, pos_tag, _ = compound_item.split("/")
                    yield word, pos_tag, compound_include_item

            else:
                yield compound_include_item.word, compound_include_item.pos, compound_include_item

    def gen_mecab_compound_token_feature(self):
        for idx, x in enumerate(list(self.tokenize_mecab_compound())):
            word, pos_tag, compound_include_item = x

            if (pos_tag in mecab_noun_pos):
                yield compound_include_item.word, NOUN

            if (pos_tag in mecab_verb_pos) and (word not in stop_words):
                yield word, VERB
