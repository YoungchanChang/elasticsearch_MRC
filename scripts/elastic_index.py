from app.infrastructure.database.elastic_conn import *
from app.config.settings import *


def set_wiki_index():

    result = es.indices.delete(index=elastic_index, ignore=[400, 404])
    print(result)

    body = {
          "mappings": {
            "properties": {
                "content-vector": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "l2_norm"
                },
                "title": {
                    "type": "keyword"
                },
                "first_header": {
                    "type": "keyword"
                },
                "second_header": {
                    "type": "keyword"
                },
                "content": {
                    "type": "keyword"
                }
            }
          }
        }

    ans = es.indices.create(index=elastic_index, body=body, ignore=400, )
    print(ans)


def exists_index():
    es_alias = es.indices.get_alias().keys()
    if "my-approx-knn-index-test" not in es_alias:
        set_wiki_index()

if __name__ == '__main__':

    exists_index()


