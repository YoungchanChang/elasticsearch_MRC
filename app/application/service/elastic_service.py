from app.application.interfaces.nlp import AbstractNLP
from app.application.interfaces.repository import AbstractRepository
from app.domain.entity import ElasticSearchDomain, QueryDomain


class ElasticService:
    """
    - 질의문에서 벡터값 추출
    - 질의문에서 체언과 용언만 추출
    - 질의문, 벡터값, 체언, 용언으로 엘라스틱서치에 질의
    """

    def __init__(self, elastic: AbstractRepository, nlp_model: AbstractNLP):
        self.elastic = elastic
        self.nlp_model = nlp_model

    def get_elastic_domain(self, query: str):

        """
        엘라스틱서치 질의어 처리를 엘라스틱서치 규격에 맞춰 변형해주는 메소드
        :param sentence: 질의어
        :return: 엘라스틱서치 질의시 필요한 값
        """

        _query = QueryDomain(query=query)

        embedding_vectors = self.nlp_model.get_embeddings(domain=_query)
        nouns, verbs = self.nlp_model.get_nouns_verbs(domain=_query)
        elastic_domain = ElasticSearchDomain(query=query, query_vector=embedding_vectors, noun_tokens=nouns,
                                             verb_tokens=verbs)
        return elastic_domain

    def insert_data(self, sentence: str):

        """
        엘라스틱서치에 삽입하는 메소드
        :param sentence:
        :return:
        """

        _elastic_domain = self.get_elastic_domain(query=sentence)
        elastic_results = self.elastic.create(domain=_elastic_domain)
        return elastic_results

    def search(self, sentence: str):

        """
        엘라스틱서치에서 질의로 검색된 문장을 가져오는 메소드
        :param sentence: 질의어
        :return: 검색된 문장 정보
        """

        _elastic_domain = self.get_elastic_domain(query=sentence)
        elastic_results = self.elastic.read(domain=_elastic_domain)
        return elastic_results


