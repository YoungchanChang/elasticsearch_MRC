import app.infrastructure.api.wiki_repo as w_r
from app.infrastructure.database.elastic_conn import es
from app.application.interfaces.repository import AbstractRepository
from app.application.service.elastic_service import ElasticService
from app.controller.elastic_controller import get_content_template, get_es_index_source
from app.domain.entity import ElasticSearchDomain, ElasticIndexDomain, WikiTitle

from app.config.settings import *
import app.infrastructure.nlp_model.nlp as p_r
import uuid
json_header = {'Content-Type': 'application/json'}


class ElasticRepository(AbstractRepository):

    def create(self, domain: ElasticIndexDomain):
        """
        엘라스틱서치에 한 문서를 넣는 기능
        :param domain: 엘라스틱서치 인덱스 규격에 맞는 데이터
        :return: 저장 결과
        """
        es_idx_data = ElasticIndexDomain(content_vector=domain.content_vector,
                                         title=domain.title, first_header=domain.first_header, second_header=domain.second_header,
                                         content=domain.content,
                                         content_noun_tokens=domain.content_noun_tokens, content_verb_tokens=domain.content_verb_tokens)

        es_idx_dict_form = get_es_index_source(es_data=es_idx_data)
        result = es.create(index=elastic_vector_index, id=str(uuid.uuid1()),document=es_idx_dict_form)
        return result

    def read(self, domain: ElasticSearchDomain):
        """
        엘라스틱서치에 질의 검색 결과를 반환하는 기능
        :param domain: 엘라스틱서치 검색 규격에 맞는 데이터
        :return: 검색결과 중 매치되는 결과
        """
        body_template = get_content_template(query=domain.query,
                                             query_vector=domain.query_vector,
                                             noun_tokens=domain.noun_tokens,
                                             verb_tokens=domain.verb_tokens)
        result = es.search(index=elastic_vector_index,
                           body=body_template)
        resp = result.body
        return resp['hits']['hits']


if __name__ == "__main__":
    pororo_mecab = p_r.PororoMecab()
    wiki_repo = w_r.WikipediaRepository(nlp_model=pororo_mecab)
    title = "조선"
    wiki_title = WikiTitle(title=title)


    elastic_repo = ElasticRepository()
    # ElasticIndexDomain(content_vector=)
    a = ElasticService(elastic=elastic_repo, nlp_model=pororo_mecab)
    print(a.search("성종의 업적이 뭐야"))