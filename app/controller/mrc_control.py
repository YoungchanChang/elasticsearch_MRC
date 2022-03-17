import json
import numpy as np
import requests

from requests.auth import HTTPBasicAuth
from pororo import Pororo

se = Pororo(task="sentence_embedding", lang="ko")
json_header = {'Content-Type':'application/json'}
mrc = Pororo(task="mrc", lang="ko")

MRC_TOKEN_SENTENCE_LIMIT = 5

def get_question_template(question: str) -> dict:
    question_val = se(question)
    pororo_list = np.array(question_val).tolist()

    field = {
      "knn": {
        "field": "content-vector",
        "query_vector": pororo_list,
        "k": 10,
        "num_candidates": 12
      },
      "fields": [
        "content-vector",
        "content"
      ]
    }
    return field


def get_elasticsearch_knn(question: str):

    resp = requests.get("https://localhost:9200/my-approx-knn-index-test/_knn_search",
                         json=get_question_template(question),
                        headers=json_header,
                         auth=HTTPBasicAuth("elastic", "6bXz4stf_*78WWZgiDPH"),
                         verify=False)

    resp = (json.loads(resp.text))

    content = []
    for idx, hit in enumerate(resp['hits']['hits']):
        content.append(hit["_source"]['content'])

    return content


def get_pororo_answer(question: str):
    content = get_elasticsearch_knn(question=question)
    mrc_answer = mrc(
       question,
       " ".join(content[:MRC_TOKEN_SENTENCE_LIMIT])
    )
    return mrc_answer


if __name__ == "__main__":
    print(get_pororo_answer("조선시대 최고 학부는 어디야"))
