from app.infrastructure.database.elastic_conn import *
from app.config.settings import *


def set_wiki_index(elastic_index: str):

    result = es.indices.delete(index=elastic_index, ignore=[400, 404])
    print(result)

    body = {
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "nori_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer",
                            "filter": [
                                "part_of_speech_stop_sp",
                            ]
                        },
                        "nori_elastic_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer",
                            "filter": [
                                "part_of_speech_stop_sp",
                            ]
                        }
                    },
                    # 동의어 추가 및 제거할 단어
                    "filter": {
                        "part_of_speech_stop_sp": {
                            "type": "nori_part_of_speech",
                            "stoptags": [
                                "E",
                                "IC",
                                "J",
                                "MAG", "MAJ", "MM",
                                "SP", "SSC", "SSO", "SC", "SE",
                                "XPN", "XSA", "XSN", "XSV",
                                "UNA", "NA", "VSV"
                            ]
                        }
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "content-vector": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine"
                },
                "title": {
                    "type": "text",
                    "analyzer": "nori_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    },
                },
                "first_header": {
                    "type": "text",
                    "analyzer": "nori_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    },
                },
                "second_header": {
                    "type": "text",
                    "analyzer": "nori_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    },

                },
                "content": {
                    "type": "text",
                    "analyzer": "nori_analyzer",
                    "fielddata": True
                }
            }
        }
    }

    ans = es.indices.create(index=elastic_index, body=body, ignore=400, )
    print(ans)


def exists_index():
    es_alias = es.indices.get_alias().keys()
    if "wiki-vector-index" not in es_alias:
        set_wiki_index()

if __name__ == '__main__':

    set_wiki_index(elastic_vector_index)

