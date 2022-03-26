from typing import List

K_NEAR_NUM = 10
NUM_CANDIDATE = 12
CONTENT_LIMIT = 3
elastic_script_formula = "(Math.log10(_score + 1)*2) + (cosineSimilarity(params.queryVector, 'content-vector') + 2.0)"


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
                                        "boost": 10
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
                                        "boost": 2
                                    }
                                }
                            },

                        ],
                },
              },
            "script": {
                "source": "_score",
                "params": {
                    "queryVector": k
                }
            },

            },

        },
        "explain": "true"
    }
    return body

def get_content_template(title: str, query: str, k: List, mecab_noun_tokens: List, mecab_verb_tokens: List):
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
                                        "boost": 2
                                    }
                                }
                            },
                            {
                                "constant_score": {
                                    "filter": {
                                        "terms": {
                                            "content_noun": [mecab_noun_tokens[0]]
                                        },
                                    },
                                    "boost": 10
                                },
                            },
                            {
                                "constant_score": {
                                    "filter": {
                                        "terms": {
                                            "content_noun": [mecab_noun_tokens[1]]
                                        },
                                    },
                                    "boost": 10
                                },
                            },
                            {
                                "constant_score": {
                                    "filter": {
                                        "terms": {
                                            "content_noun": mecab_verb_tokens
                                        },
                                    },
                                    "boost": 10

                                },
                            },
                        ],
                },
              },
            "script": {
                "source": elastic_script_formula,
                "params": {
                    "queryVector": k
                }
            },

            },

        },
        "explain": "true"
    }
    return body
