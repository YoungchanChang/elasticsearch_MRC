from typing import List
import re

import numpy as np

from pororo import Pororo
from typing import Generator
from kss import split_sentences

from app.application.elastic_service import ElasticService
from app.application.mecab_service import get_pos_idx, MecabInflectParser, filter_necessary
from app.config.settings import *
from app.application.wikipedia_service import WikipediaService
from app.domain.domain import WikiItem
from app.domain.elastic_domain import get_content_template, get_title_template
from app.infrastructure.api.wiki_repo import WikiContent

import app.infrastructure.database.elastic_repository as el_repo

se = Pororo(task="sentence_embedding", lang="ko")
mrc = Pororo(task="mrc", lang="ko")

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



class WikiControl:

    def get_wiki_data(self, title: str) -> Generator:

        """
        위키피디아 데이터 검색 후 값 가져오는 함수
        :param title: 검색 키워드
        :return: 검색 후 템플릿으로 변경
        """
        wiki_content = WikiContent()
        page_py = WikipediaService(wiki_content).get_wiki_data(title)
        for page_item in split_sentences(page_py.summary):
            yield WikiItem(title=page_py.title,
                           first_header=page_py.title,
                           second_header=page_py.title,
                           content=page_item)

        for page_section in page_py.sections:
            for page_sec_item in page_section.sections:

                for page_test_item in page_sec_item.text.split("\n"):
                    if page_test_item == "" or page_test_item == "\t\t":
                        continue
                    for page_item_one_sentence in split_sentences(page_test_item):
                        yield WikiItem(title=page_py.title,
                                       first_header=page_section.title,
                                       second_header=page_sec_item.title,
                                       content=page_item_one_sentence)

    def gen_vector_data(self, title):
        from collections import defaultdict
        d = defaultdict(list)
        for wiki_item in self.get_wiki_data(title):
            dic_key = wiki_item.title + "@@@" + wiki_item.first_header + "@@@" + wiki_item.second_header
            d[dic_key].append(wiki_item.content)


        for d_key in d.keys():
            d_list = d[d_key]
            for idx, d_item in enumerate(d_list):
                item_pos = get_pos_idx(d_item)

                if item_pos[0][1] in ["NP", 'MM', 'MAJ']:
                    d_item = d_list[idx-1] + " " + d_item

                elif item_pos[0][0] in ['이후', '한편']:
                    d_item = d_list[idx - 1] + " " +d_item

                title, first_header, second_header = d_key.split("@@@")
                header = title + " " + title + " " + title + " " + first_header + " " + first_header + " " + second_header
                mecab_inflect_result = [x[0] for x in list(MecabInflectParser(header + d_item).gen_mecab_compound_token_feature())]
                extracted_data = " ".join(mecab_inflect_result)
                print(extracted_data)
                content_vector = encode_vectors(extracted_data)

                yield {
                    "_index": elastic_vector_index,
                    "_source": {
                            "content-vector": content_vector,
                            "title": title,
                            "first_header": first_header,
                            "second_header": second_header,
                            "content": d_item
                        }
                    }


def encode_vectors(question: str) -> List:
    se_val = se(" ".join(question))
    return np.array(se_val).tolist()


def get_encoded_title_template(question: str) -> dict:
    """
    컨텐츠 벡터값 인코딩을 위한 템플릿
    :param title:
    :param question:
    :return:
    """
    question_vector = encode_vectors(question=question)

    content_template = get_title_template(question, question_vector)

    return content_template


def get_encoded_content_template(title: str, question: str) -> dict:
    """
    컨텐츠 벡터값 인코딩을 위한 템플릿
    :param title:
    :param question:
    :return:
    """
    question_vector = encode_vectors(question=question)

    content_template = get_content_template(title, question, question_vector)

    return content_template

class MRC:

    def filter_elastic_data(self, elastic_content: List):
        content = []
        vector_content = []
        for idx, hit in enumerate(elastic_content):
            if hit['_score'] > 1:
                content.append(hit["_source"])
            else:
                vector_content.append(hit["_source"])

        if len(content) == 0:
            content.extend(vector_content)

        return content

    def get_elastic_content(self, question: str):
        content_repository = el_repo.ElasticContent()
        title_repository = el_repo.ElasticTitle()
        elastic_service = ElasticService(title_repository, content_repository)

        elastic_content = elastic_service.get_content(question)
        filtered_elastic_content = self.filter_elastic_data(elastic_content)

        return filtered_elastic_content

    def filter_mrc_content(self, question: str):
        elastic_content = self.get_elastic_content(question=question)
        title = elastic_content[BEST_VALUE]["title"]
        elastic_content = [x["content"] for x in elastic_content]

        mrc_sentence = f"{SENTENCE_SPLIT_SYMBOL}".join(elastic_content)

        mrc_answer = mrc(
           filter_necessary(question),
           mrc_sentence
        )

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
    mrc = MRC()
    print(mrc.get_elastic_content("조선시대 최고 학부는 어디야"))
