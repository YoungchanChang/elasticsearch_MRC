from app.application.interfaces.nlp import AbstractNLP
from app.application.interfaces.repository import AbstractRepository
from app.domain.entity import KeywordVectorDomain, QueryDomain


class KeywordVectorRepository:

    """ 키워드와 벡터값을 활용한 데이터베이스

    질의문에서 벡터값과 키워드(체언과 용언)을 추출한 뒤에 데이터베이스에 입, 출력을 한다.

    주요 메소드:

    - _get_keyword_vector_domain() : 질의문에서 벡터값 추출
    - create() : 데이터베이스 삽입
    - read() : 데이터베이스 읽질의문, 벡터값, 체언, 용언으로 데이터베이스에 삽입,
    """

    def __init__(self, repository: AbstractRepository, nlp_model: AbstractNLP):
        self.repository = repository
        self.nlp_model = nlp_model

    def _get_keyword_vector_domain(self, query: str) -> KeywordVectorDomain:

        """쿼리로부터 벡터값과 키워드를 추출하는 메소드

        이 함수는 질의어로부터 임베딩 벡터값과, 체언형 키워드, 용언형 키워드를 추출하는 기능을 한다.

        :param query: 질의어
        :return: 키워드벡터 도메인
        """

        _query = QueryDomain(query=query)

        embedding_vectors = self.nlp_model.get_embeddings(domain=_query)
        nouns, verbs = self.nlp_model.get_nouns_verbs(domain=_query)
        keyword_vector_domain = KeywordVectorDomain(query=query, query_vector=embedding_vectors, noun_tokens=nouns,
                                             verb_tokens=verbs)
        return keyword_vector_domain

    def create(self, query: str):

        """질의어로부터 추출된 정보를 데이터베이스에 저장하는 메소드
        :param query: 질의어
        :return: 데이터 삽입 결과
        """

        _keyword_vector_domain = self._get_keyword_vector_domain(query=query)
        insert_results = self.repository.create(domain=_keyword_vector_domain)
        return insert_results

    def read(self, query: str):

        """질의어로부터 추출된 정보를 바탕으로 데이터베이스 정보를 추출하는 메소드
        :param query: 질의어
        :return: 데이터 추출 결과
        """

        _keyword_vector_domain = self._get_keyword_vector_domain(query=query)
        read_results = self.repository.read(domain=_keyword_vector_domain)
        return read_results


