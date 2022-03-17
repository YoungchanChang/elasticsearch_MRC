import json
import numpy as np
import requests

from requests.auth import HTTPBasicAuth
from pororo import Pororo


from app.application.wikipedia_data import get_wiki_data
from app.domain.elastic_domain import get_knn_template
from main import elastic_index

se = Pororo(task="sentence_embedding", lang="ko")
json_header = {'Content-Type':'application/json'}
mrc = Pororo(task="mrc", lang="ko")

MRC_TOKEN_SENTENCE_LIMIT = 5


def gen_mrc_data(keyword):

    """
    mrc에 데이터 삽입하는 함수
    :param keyword:
    :return:
    """

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


class MRC:

    def get_question_template(self, question: str) -> dict:
        question_val = se(question)
        pororo_list = np.array(question_val).tolist()

        field = get_knn_template(pororo_list)

        return field


    def get_elasticsearch_knn(self, question: str):

        resp = requests.get("https://localhost:9200/my-approx-knn-index-test/_knn_search",
                             json=self.get_question_template(question),
                            headers=json_header,
                             auth=HTTPBasicAuth("elastic", "6bXz4stf_*78WWZgiDPH"),
                             verify=False)

        resp = (json.loads(resp.text))

        content = []
        for idx, hit in enumerate(resp['hits']['hits']):
            content.append(hit["_source"]['content'])

        return content


    def get_pororo_answer(self, question: str):
        content = self.get_elasticsearch_knn(question=question)
        mrc_answer = mrc(
           question,
           " ".join(content[:MRC_TOKEN_SENTENCE_LIMIT])
        )
        return mrc_answer


if __name__ == "__main__":
    mrc = MRC()
    print(mrc.get_pororo_answer("조선시대 최고 학부는 어디야"))
