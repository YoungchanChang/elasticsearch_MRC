from app.application.repo_interface import AbstractRepository
from app.config.settings import elastic_index
from app.controller.mrc_control import gen_mrc_data
from app.domain.custome_error import WikiDataException
from app.domain.domain import WikiQuestionItemDTO
from app.domain.elastic_domain import get_es_title_template
from app.infrastructure.database.elastic_conn import es
from elasticsearch import helpers


class WikiSearch(AbstractRepository):

    def create(self, model: WikiQuestionItemDTO):
        """
        위키피디아에서 검색 후 데이터 생성
        :param model: 위키피디아 주제, 질문 데이터
        :return:
        """
        result = helpers.bulk(es, gen_mrc_data(model.title))
        return result

    def find_one(self, model: WikiQuestionItemDTO):

        """
        제목 찾고 없으면 위키피디아에서 검색 후 생성
        :param model: 위키피디아 주제, 질문 데이터
        :return: 성공 여부
        """

        result = es.search(index=elastic_index, body=get_es_title_template(model.title))
        hit_len = len(result.body['hits']['hits'])
        if hit_len == 0:
            # 없으면 생성, 못 찾으면 에러 반환
            self.create(model)
        return result


if __name__ == "__main__":
    wiki_question = WikiQuestionItemDTO(title="조선ㅇㅇㅇ", question="조선 최고 학당이 어디야?")
    wiki_search = WikiSearch()
    wiki_result = wiki_search.find_one(wiki_question)
    wiki_final_result = wiki_result.body['hits']['hits']
    print(wiki_result)
    print(wiki_final_result)
