from typing import List

from app.controller.adapter.elastic_dto import ElasticFieldDto

FIELD = 0
BOOST = 1
NOUN_BOOST = 10
VERB_BOOST = 5
CONTENT_LIMIT = 5

source_fields = ["title", "first_header", "second_header", "content"]
boost_fields = [1, 1, 1, 2]

elastic_script_formula = f"(Math.log10(_score + 1)) * (cosineSimilarity(params.queryVector, 'content_vector') + 2.0)"


def get_elastic_terms_dict(search_field: str, term_token: str, boost: int):
    """키워드 매칭 점수 추출을 위한 엘라스틱서치 질의어 필드
    :param search_field: 키워드를 매칭 필드
    :param term_token: 키워드 토큰
    :param boost: 키워드 필드별 가중치
    :return: 매칭 점수를 위한 딕셔너리 클래스
    """
    elastic_query = {
        "constant_score": {
            "filter": {
                "terms": {
                    search_field: [term_token, ]
                },
            },
            "boost": boost
        },
    }
    return elastic_query


def get_match_dict(query: str, field: str, boost: int):

    """BM25 텍스트 매칭 점수를 위한 엘라스틱서치 질의어 필드
    :param query: 질의어
    :param field: 텍스트 필드
    :param boost: 가중치
    :return: 질의어별 가중치
    """

    should_match = {
        "match": {
            field: {
                "query": query,
                "boost": boost
            }
        }
    }
    return should_match


def get_content_template(query: str, query_vector: List, noun_tokens: List, verb_tokens: List):

    """엘라스틱서치 키워드, 벡터값 질의를 위한 템플릿 반환 함수

    :param query:
    :param query_vector:
    :param noun_tokens:
    :param verb_tokens:
    :return:
    """

    should_list = []
    for noun_token in noun_tokens:
        should_list.append(get_elastic_terms_dict("content_noun_search", noun_token, NOUN_BOOST))

    for verb_token in verb_tokens:
        should_list.append(get_elastic_terms_dict("content_verb_search", verb_token, VERB_BOOST))

    for zip_item in zip(source_fields, boost_fields):
        should_list.append(get_match_dict(query, zip_item[FIELD], zip_item[BOOST]))

    body = {
        "size": CONTENT_LIMIT,
        "_source": source_fields,
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "should": should_list,
                    },
                },
                "script": {
                    "source": elastic_script_formula,
                    "params": {
                        "queryVector": query_vector
                    }
                },

            },

        },
        "explain": "true"
    }
    return body


def get_es_index_source(es_data: ElasticFieldDto):

    """엘라스틱서치

    :param es_data:
    :return:
    """

    return {
            "content_vector": es_data.content_vector,
            "title": es_data.title,
            "first_header": es_data.first_header,
            "second_header": es_data.second_header,
            "content": es_data.content,
            "content_noun_search": es_data.content_noun_tokens,
            "content_verb_search": es_data.content_verb_tokens,
    }

def get_es_index_template(elastic_index: str, es_data: ElasticFieldDto):
    return {
        "_index": elastic_index,
        "_source": get_es_index_source(es_data=es_data)
    }

