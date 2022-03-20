from typing import List

K_NEAR_NUM = 10
NUM_CANDIDATE = 12
CONTENT_LIMIT = 5


def get_knn_template(k: List):

    elastic_search_field = {
          "knn": {
            "field": "title-vector",
            "query_vector": k,
            "k": K_NEAR_NUM,
            "num_candidates": NUM_CANDIDATE
          },
          "fields": [
            "title",
            "first_header",
            "second_header",
          ]
        }

    return elastic_search_field

def get_title_template(query: str, k: List):
    body = {
        "size": CONTENT_LIMIT,
        "_source": ["title", "first_header", "second_header", "content"],
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "should":[
                            {
                                "match": {
                                    "title": {
                                        "query": query,
                                        "boost": 5
                                    }
                                }
                            },
                            {
                                "match": {
                                    "first_header": {
                                        "query": query,
                                    }
                                }
                            },
                            {
                                "match": {
                                    "second_header": {
                                        "query": query,
                                    }
                                }
                            },
                            {
                                "match": {
                                    "content": {
                                        "query": query,
                                    }
                                }
                            },
                        ],
                },
              },
            "script": {
                "source": "_score * (cosineSimilarity(params.queryVector, 'content-vector') + 1.0)",
                "params": {
                    "queryVector": k
                }
            },

            },

        },
        "explain": "true"
    }
    return body

def get_content_template(title: str, query: str, k: List):
    body = {
        "size": CONTENT_LIMIT,
        "_source": ["title", "first_header", "second_header", "content"],
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "filter": {
                            "match": {
                                "title.keyword": title,
                            },

                        },
                        "should":[
                            {
                                "match": {
                                    "first_header": {
                                        "query": query,
                                    }
                                }
                            },
                            {
                                "match": {
                                    "second_header": {
                                        "query": query,
                                    }
                                }
                            },
                            {
                                "match": {
                                    "content": {
                                        "query": query,
                                    }
                                }
                            },
                        ],
                },
              },
            "script": {
                "source": "_score * (cosineSimilarity(params.queryVector, 'content-vector') + 1.0)",
                "params": {
                    "queryVector": k
                }
            },

            },

        },
        "explain": "true"
    }
    return body
