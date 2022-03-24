import copy
from typing import List, Generator
import mecab
from python_mecab_ner.mecab_parser import MecabParser

mecab = mecab.MeCab()

NOUN = "Noun"
VERB = "Verb"

mecab_all_pos = ["NNG", "NNP", "NNB", "NNBC", "NR", "NP",
                   "VV", "VA", "VX", "VCP", "VCN",
                   "MM", "MAG", "MAJ",
                   "IC",
                   "JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC",
                   "EP", "EF", "EC", "ETN", "ETM",
                   "XPN", "XSN", "XSV", "XSA", "XR",
                   "SF", "SE", "SSO", "SSC", "SC", "SY", "SL", "SH", "SN"]

mecab_pos_allow = [
                "NNG", "NNP", "NR",
                "VV", "VA", "VX",
                "XPN", "XR",
                "MM",
                "SL", "SH", "SN",]

mecab_noun_pos = ["NNG", "NNP",
                  "MM",
                  "XR",
                  "SL", "SH", "SN" 
                  "UNKOWN"]


mecab_verb_pos = ["VV", "VA"]


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

            if (pos_tag in mecab_noun_pos):
                yield compound_include_item.word, NOUN

            if (pos_tag in mecab_verb_pos) and (word not in stop_words):
                yield word, VERB

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
    d_item = "잡혔었었다."
    for i in list(MecabInflectParser("김보당은 정중부에게 붙잡혔다.").gen_mecab_compound_token_feature()):
        print(i)
    mecab_tokens = list(MecabInflectParser(d_item).gen_mecab_compound_token_feature())
    print(mecab_tokens)
    mecab_noun_tokens = [x[0] for x in mecab_tokens if x[1] == NOUN]
    print(mecab_noun_tokens)
    mecab_verb_tokens = [x[0] for x in mecab_tokens if x[1] == VERB]
    print(mecab_verb_tokens)