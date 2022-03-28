import re
from typing import List

from app.application.interfaces.nlp import AbstractNLP
from app.application.interfaces.repository import AbstractRepository
from app.application.service.keyword_vector_repository import KeywordVectorRepository
from app.controller.adapter.elastic_dto import ElasticParsingResult
from app.domain.entity import MrcDomain


def parse_elastic_data(elastic_item: dict) -> ElasticParsingResult:

    """엘라스틱서치 데이터에서 필요한 데이터만 추출하는 함수
    :param elastic_item: 엘라스틱서치 hits된 아이템 정보
    :return: 아이템 정보중 필요한 필드만 추출
    """

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


class ElasticMrcController(KeywordVectorRepository):

    ITEM_SENTENCE = 1
    ITEM_LENGTH = 2
    BEST_VALUE = 0
    MRC_ANSWER = 0
    MRC_INDEX = 1
    MRC_NOT_FOUND = ''
    END_IDX = 1

    SENTENCE_SPLIT_SYMBOL = "@"

    def __init__(self, repository: AbstractRepository, nlp_model: AbstractNLP):

        super().__init__(repository=repository, nlp_model=nlp_model)
        self.nlp_model = nlp_model
        self.repository = repository

    def put_mrc_content(self, question: str):
        result = self.create(query=question)
        return result

    def get_content(self, question: str):
        elastic_content = self.read(query=question)
        return elastic_content

    def get_mrc_candidates(self, elastic_contents: List):

        """ 엘라스틱서치 파싱 내용 중 mrc에 질의하기 위한 메소드
        :param elastic_contents: 엘라스틱서치 검색 내용
        :return: mrc원본 정보, 문장 정보, 문장 길이
        """

        for idx, items in enumerate(elastic_contents):
            symbol_idx = ""
            if len(elastic_contents) != (idx+1):
                symbol_idx = self.SENTENCE_SPLIT_SYMBOL*(idx+1)
            mrc_item = items.content + " " + symbol_idx + " "
            item_length = len(mrc_item)
            yield mrc_item, items.content, item_length

    def get_mrc_idx(self, mrc_answer: tuple, mrc_cand_list: List):

        """엘라스틱서치 검색 결과 중 mrc 인덱스 후보군 추출
        :param mrc_answer: mrc에서 추출한 답변
        :param mrc_cand_list: mrc에서 답변을 추출할 후보군
        :return: mrc에 매칭된 문장, 후보군에서 매칭된 인덱스 값, 답변이 추론 범위에 있었는지
        """

        total_length = 0
        end_pos = mrc_answer[self.MRC_INDEX][self.END_IDX]
        mrc_matching_sentence = ''
        cand_hit_idx = 0
        answer_found = False
        for idx, mrc_cand_item in enumerate(mrc_cand_list):
            total_length += mrc_cand_item[self.ITEM_LENGTH]
            if end_pos < total_length:
                mrc_matching_sentence = mrc_cand_item[self.ITEM_SENTENCE]
                cand_hit_idx = idx

                if mrc_answer[self.MRC_ANSWER] in mrc_cand_item[self.ITEM_SENTENCE]:
                    answer_found = True
                    break

        return mrc_matching_sentence, cand_hit_idx, answer_found

    def get_mrc_content(self, question: str, elastic_contents: List):

        """질의문 중에 엘라스틱서치 검색 결과와 가장 가까운 문장을 찾는 메소드

        MRC를 통해 답변을 찾은 뒤, 답변의 위치가 포함된 문장을 반환한다.

        :param question: 질의문
        :param elastic_contents: MRC에 넣을 엘라스틱서치 문장
        :return: mrc매칭 단어, mrc 매칭 문장, 엘라스틱서치중 mrc답변이 포함된 문장
        """

        elastic_contents = [parse_elastic_data(x) for x in elastic_contents]

        mrc_cand_list = list(self.get_mrc_candidates(elastic_contents=elastic_contents))

        mrc_candidates = [x[self.BEST_VALUE] for x in mrc_cand_list]
        mrc_sentence = f"".join(mrc_candidates)
        mrc_domain = MrcDomain(question, mrc_sentence)
        mrc_answer = self.nlp_model.predict(domain=mrc_domain)

        mrc_hit_words = mrc_answer[self.MRC_ANSWER]

        mrc_matching_sentence, elastic_hit_idx, answer_found = self.get_mrc_idx(mrc_answer=mrc_answer, mrc_cand_list=mrc_cand_list)

        if (mrc_hit_words == self.MRC_NOT_FOUND) or answer_found is False:
            return "NotHit", elastic_contents[self.BEST_VALUE].content, elastic_contents[self.BEST_VALUE]

        return mrc_hit_words, mrc_matching_sentence, elastic_contents[elastic_hit_idx]