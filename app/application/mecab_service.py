import copy
from typing import List, Generator
import mecab
from python_mecab_ner.mecab_parser import MecabParser

mecab = mecab.MeCab()

mecab_pos_allow = [
                "NNG", "NNP", "NR",
                "VV", "VA", "VX",
                "XPN", "XR",
                "MM",
                "SL", "SH", "SN",]


stop_words = ['하']

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

            if (pos_tag in mecab_pos_allow) and (word not in stop_words):
                x = (compound_include_item.word, pos_tag)
                yield x


def filter_necessary(question: str) -> str:
    mecab_parsed = mecab.parse(question)
    answer = []
    for i in mecab_parsed:
        i_post = i[1].pos.split("+")
        if any(elem in i_post for elem in mecab_pos_allow):
            answer.append(i[0])

    return " ".join(answer)


def get_pos_idx(question: str) -> List:
    mecab_parsed = mecab.parse(question)
    return [(x[0], x[1].pos) for x in mecab_parsed]


if __name__ == "__main__":
    for i in list(MecabInflectParser("밥을 정말 맛있게 먹었다").gen_mecab_compound_token_feature()):
        print(i)
