from typing import List

from app.domain.entity import ElasticIndexDomain

FIELD = 0
BOOST = 1
NOUN_BOOST = 10
VERB_BOOST = 5
CONTENT_LIMIT = 3

source_fields = ["title", "first_header", "second_header", "content"]
boost_fields = [1, 1, 1, 2]

elastic_script_formula = "(Math.log10(_score + 1)*2) + (cosineSimilarity(params.queryVector, 'content_vector') + 2.0)"


def get_elastic_term_dict(noun_token: str, boost: int):
    elastic_query = {
        "constant_score": {
            "filter": {
                "terms": {
                    "content_noun": [noun_token,]
                },
            },
            "boost": boost
        },
    }
    return elastic_query


def get_match_query(query: str, field: str, boost: int):
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
    should_list = []
    for noun_token in noun_tokens:
        should_list.append(get_elastic_term_dict(noun_token, NOUN_BOOST))

    for verb_token in verb_tokens:
        should_list.append(get_elastic_term_dict(verb_token, VERB_BOOST))

    for zip_item in zip(source_fields, boost_fields):
        should_list.append(get_match_query(query, zip_item[FIELD], zip_item[BOOST]))

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


def get_es_index_template(elastic_index: str, es_data: ElasticIndexDomain):
    return {
        "_index": elastic_index,
        "_source": get_es_index_source(es_data=es_data)
    }

def get_es_index_source(es_data: ElasticIndexDomain):
    return {

            "content_vector": es_data.content_vector,
            "title": es_data.title,
            "first_header": es_data.first_header,
            "second_header": es_data.second_header,
            "content": es_data.content,
            "content_noun_search": es_data.content_noun_tokens,
            "content_verb_search": es_data.content_verb_tokens,
    }