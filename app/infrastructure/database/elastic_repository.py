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
        result = helpers.bulk(es, gen_mrc_data(model.title))
        return result

    def find_one(self, model: WikiQuestionItemDTO):
        result = es.search(index=elastic_index, body=get_es_title_template(model.title))
        hit_len = len(result.body['hits']['hits'])
        if hit_len == 0:
            raise WikiDataException("위키피디아 데이터 없음")
        return result


if __name__ == "__main__":
    wiki_question = WikiQuestionItemDTO(title="조선ㅇㅇㅇ", question="조선 최고 학당이 어디야?")
    wiki_search = WikiSearch()
    wiki_result = wiki_search.find_one(wiki_question)
    wiki_final_result = wiki_result.body['hits']['hits']
    print(wiki_result)
    print(wiki_final_result)
