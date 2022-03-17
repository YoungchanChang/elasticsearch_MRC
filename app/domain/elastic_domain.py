from typing import List

K_NEAR_NUM = 10
NUM_CANDIDATE = 12
ONLY_ONE_TITLE = 1


def get_knn_template(k: List):

    elastic_search_field = {
          "knn": {
            "field": "content-vector",
            "query_vector": k,
            "k": K_NEAR_NUM,
            "num_candidates": NUM_CANDIDATE
          },
          "fields": [
            "content-vector",
            "content"
          ]
        }

    return elastic_search_field


def get_es_title_template(keyword: str):
    body = {
        "size": ONLY_ONE_TITLE,
        "_source": ["title"],
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "title": {
                                "query": keyword,
                            }
                        }
                    },

                ]
            }
        },
        "explain": "true"
    }
    return body