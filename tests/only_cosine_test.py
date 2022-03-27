import re

from app.application.service.elastic_service import ElasticService
from app.config.settings import elastic_vector_index
from app.domain.entity import ElasticIndexDomain, QueryDomain, ElasticSearchDomain
from app.infrastructure.database.elastic_repository import ElasticRepository
from app.infrastructure.nlp_model.nlp import PororoMecab, ElasticMrc
from scripts.elastic_vector_index import set_wiki_index
import csv

title = "test"
content_noun_tokens = ["철수", "영희"]
content_verb_tokens = []

es_repo = ElasticRepository()
pororo_nlp = PororoMecab()

def put_test_data():

    with open("./test_data/only_cosine_question.txt", "r", encoding='utf-8-sig') as file:
        test_all_query = file.read().splitlines()
        for query in test_all_query:
            _query = QueryDomain(query=query)
            embedding_vectors = pororo_nlp.get_embeddings(domain=_query)

            elastic_index_domain = ElasticIndexDomain(content_vector=embedding_vectors, title=title, first_header=title,
                                                      second_header=title,
                                                      content=query,
                                                      content_noun_tokens=content_noun_tokens,
                                                      content_verb_tokens=content_verb_tokens)
            es_repo.create(elastic_index_domain)



if __name__ == "__main__":
    # 하나의 문서만 데이터 삽입

    # 벡터값을 구한다, nouns에는 일부만 저장한다.
    # set_wiki_index(elastic_vector_index)
    # put_test_data()

    # 키워드 강제 조정
    query = "철수랑 영희가 언제 집에 있었지"
    _query = QueryDomain(query=query)
    embedding_vectors = pororo_nlp.get_embeddings(domain=_query)
    elastic_domain = ElasticSearchDomain(query="", query_vector=embedding_vectors,
                                         noun_tokens=content_noun_tokens,
                                         verb_tokens=content_verb_tokens)
    elastic_repo = ElasticRepository()
    read_data = elastic_repo.read(domain=elastic_domain)
    elastic_mrc = ElasticMrc()

    elastic_content = elastic_mrc.get_content(question=query)
    value = elastic_mrc.get_mrc_content(question=query, elastic_contents=elastic_content)
    print(query, value)
    with open('./test_data/only_cosine_result.csv', 'a', encoding='utf-8-sig', newline='') as writer_csv:

        for read_item in read_data:
            elastic_parsing_result = elastic_mrc.extract_elastic_data(elastic_item=read_item)
            print(elastic_parsing_result)
            writer = csv.writer(writer_csv, delimiter=',')

            # 3. write row
            writer.writerow([elastic_parsing_result.score, elastic_parsing_result.content])
        writer.writerow([query, value[0], value[1]])