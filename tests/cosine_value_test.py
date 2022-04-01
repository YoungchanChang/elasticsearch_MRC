import re

from app.controller.adapter.elastic_dto import ElasticFieldDto
from app.controller.elastic_controller import parse_elastic_data, ElasticMrcController
from app.domain.entity import KeywordVectorDomain, QueryDomain
from app.infrastructure.database.elastic_repository import ElasticRepository
from app.infrastructure.nlp_model.nlp import PororoMecab
import csv

title = "test"
content_noun_tokens = ["철수", "영희"]
content_verb_tokens = []

es_repo = ElasticRepository()
pororo_nlp = PororoMecab()

def put_test_data():
    import pandas as pd

    df = pd.read_excel("./test_data/wellness_talk_dataset.xlsx")

    df = df[~df['챗봇'].isna()]

    for i in df.values:
        print(i[1])
    # with open("./test_data/only_cosine_question.txt", "r", encoding='utf-8-sig') as file:
    #     test_all_query = file.read().splitlines()
    #     for query in test_all_query:
    #     _query = QueryDomain(query=i[1])
    #     embedding_vectors = pororo_nlp.get_embeddings(domain=_query)
    #
    #     elastic_index_domain = ElasticFieldDto(content_vector=embedding_vectors, title=title, first_header=title,
    #                                            second_header=title,
    #                                            content=i[2],
    #                                            content_noun_tokens=content_noun_tokens,
    #                                            content_verb_tokens=content_verb_tokens)
    #     es_repo.create(elastic_index_domain)
    #


if __name__ == "__main__":
    # 하나의 문서만 데이터 삽입

    # 벡터값을 구한다, nouns에는 일부만 저장한다.
    # set_wiki_index(elastic_vector_index)
    # put_test_data()




    # # 키워드 강제 조정
    with open("./test_data/only_cosine_test_question.txt", "r", encoding='utf-8-sig') as file:
        test_all_query = file.read().splitlines()
        for query in test_all_query:
            print(query)
            _query = QueryDomain(query=query)
            embedding_vectors = pororo_nlp.get_embeddings(domain=_query)
            elastic_domain = KeywordVectorDomain(query="", query_vector=embedding_vectors,
                                                 noun_tokens=content_noun_tokens,
                                                 verb_tokens=content_verb_tokens)
            elastic_repo = ElasticRepository()
            # read_data = elastic_repo.read(domain=elastic_domain)
            elastic_mrc = ElasticMrcController(repository=elastic_repo, nlp_model=pororo_nlp)

            elastic_content = elastic_mrc.get_content(question=query)
            if elastic_content != []:
                value = elastic_mrc.get_mrc_content(question=query, elastic_contents=elastic_content)
            else :
                value = [" ", " "]
            print(query, value)
            with open('./test_data/only_cosine_result.csv', 'a', encoding='utf-8-sig', newline='') as writer_csv:
                # if elastic_content != []:
                #
                #     for read_item in elastic_content:
                #         if read_item == " ":
                #             continue
                #         elastic_parsing_result = parse_elastic_data(elastic_item=read_item)
                #         print(elastic_parsing_result)
                writer = csv.writer(writer_csv, delimiter=',')
                #
                #         # 3. write row
                #         writer.writerow([elastic_parsing_result.score, elastic_parsing_result.content, " "])
                writer.writerow([query, value[0], value[1]])