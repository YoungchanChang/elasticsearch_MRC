from collections import defaultdict
from typing import Generator

from app.application.interfaces.nlp import AbstractNLP
from app.application.interfaces.repository import AbstractRepository

import wikipediaapi

from app.controller.adapter.elastic_dsl import get_es_index_template
from app.controller.adapter.elastic_dto import ElasticFieldDto
from app.controller.adapter.wiki_dto import WikiTitle, WikiItem
from app.domain.custom_error import WikiDataException
from app.domain.entity import QueryDomain
from app.infrastructure.nlp_model.nlp import get_least_meaning

from app.config.settings import *
from elasticsearch import helpers
from app.infrastructure.database.elastic_conn import es

wiki_wiki = wikipediaapi.Wikipedia('ko')


def split_wiki_sentence(split_target: str):

    for sentence_line in split_target.splitlines():
        for sentence_split_item in sentence_line.split("다."):
            if sentence_split_item == '':
                continue
            print(sentence_split_item + "다.")
            yield sentence_split_item.strip() + "다."


class WikipediaRepository(AbstractRepository):

    split_symbol = "@@@"

    def __init__(self, nlp_model: AbstractNLP):
        self.nlp_model = nlp_model

    def create(self, domain: WikiTitle):
        """
        위키피디아 데이터를 엘라스틱서치에 넣는 함수
        :param domain: 위키피디아 제목
        :return: 저장 결과
        """
        result = helpers.bulk(es, self.gen_wiki_data(domain=WikiTitle(title=domain.title)))
        return result

    def read(self, domain: WikiTitle):
        """
        위키피디아 데이터 가져오는 함수
        :param domain: 위키피디아 제목
        :return: 위키피디아 API 검색 결과
        """
        page_py = wiki_wiki.page(domain.title)

        if page_py.text == '':
            raise WikiDataException("위키피디아 데이터 없음")
        return page_py

    def get_wiki_data(self, title: str) -> Generator:

        page_py = self.read(WikiTitle(title=title))

        for page_item in split_wiki_sentence(page_py.summary):
            yield WikiItem(title=page_py.title,
                           first_header=page_py.title,
                           second_header=page_py.title,
                           content=page_item)

        for page_section in page_py.sections:
            for page_sec_item in page_section.sections:

                for page_test_item in page_sec_item.text.split("\n"):
                    if page_test_item == "" or page_test_item == "\t\t":
                        continue
                    for page_item_one_sentence in split_wiki_sentence(page_test_item):
                        yield WikiItem(title=page_py.title,
                                       first_header=page_section.title,
                                       second_header=page_sec_item.title,
                                       content=page_item_one_sentence)

    def gen_wiki_data(self, domain: WikiTitle):
        d = defaultdict(list)
        for wiki_item in self.get_wiki_data(domain.title):

            dic_key = wiki_item.title + self.split_symbol + wiki_item.first_header + self.split_symbol + wiki_item.second_header
            d[dic_key].append(wiki_item.content)

        for d_key in d.keys():
            d_list = d[d_key]
            for idx, d_item in enumerate(d_list):
                item_pos = self.nlp_model.get_pos(QueryDomain(query=d_item))

                # 이전 문장 고려
                if item_pos[0][1] in ["NP", 'MM', 'MAJ']:
                    d_item = d_list[idx-1] + " " + d_item

                elif item_pos[0][0] in ['이후', '한편']:
                    d_item = d_list[idx - 1] + " " +d_item

                title, first_header, second_header = d_key.split(self.split_symbol)
                header = title + " " + title + " " + title + " " + first_header + " " + first_header + " " + second_header
                least_meaning = get_least_meaning(domain=QueryDomain(query=header + d_item))

                extracted_data = " ".join(least_meaning)

                content_vector = self.nlp_model.get_embeddings(domain=QueryDomain(query=extracted_data))
                full_content = title + " " + first_header + " " + second_header + " " + d_item

                nouns, verbs = self.nlp_model.get_nouns_verbs(domain=QueryDomain(query=full_content))
                nouns = list(set(list(nouns)))
                verbs = list(set(list(verbs)))

                es_idx_data = ElasticFieldDto(content_vector=content_vector,
                                              title=title, first_header=first_header, second_header=second_header,
                                              content=d_item,
                                              content_noun_tokens=nouns, content_verb_tokens=verbs)

                es_idx_dict_form = get_es_index_template(elastic_index=elastic_vector_index, es_data=es_idx_data)
                yield es_idx_dict_form
