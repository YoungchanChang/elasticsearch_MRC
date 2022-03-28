from dataclasses import dataclass
from typing import List


@dataclass
class Domain:
    ...


@dataclass
class QueryDomain(Domain):
    """사용자 질의문"""
    query: str


@dataclass
class KeywordVectorDomain(QueryDomain):
    """질의의 키워드와 벡터값 정보를 포함하는 데이터 클래스"""
    query_vector: List
    noun_tokens: List
    verb_tokens: List



@dataclass
class MrcDomain(QueryDomain):
    """MRC에 질의하기 위한 데이터 클래스"""
    search_string: str