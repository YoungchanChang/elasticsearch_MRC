import numpy as np

from elasticsearch import helpers

from pororo import Pororo

from app.config.settings import elastic_index
from app.controller.wikipedia_data import get_wiki_data
from app.infrastructure.database.elastic_conn import es

se = Pororo(task="sentence_embedding", lang="ko")


def gendata(keyword):

    for page_item in get_wiki_data(keyword):

        yield {
            "_index": elastic_index,
            "_source": {
                    "content-vector": np.array(se(page_item.content)).tolist(),
                    "title": page_item.title,
                    "first_header": page_item.first_header,
                    "second_header": page_item.second_header,
                    "content": page_item.content
                }
            }


def bulk_data(keyword):
    helpers.bulk(es, gendata(keyword))


if __name__ == "__main__":
    bulk_data("조선")


