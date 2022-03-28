from dataclasses import dataclass
from typing import List


@dataclass
class Domain:
    ...


@dataclass
class WikiTitle(Domain):
    title: str


@dataclass
class WikiItem(WikiTitle):
    first_header: str
    second_header: str
    content: str


@dataclass
class QueryDomain(Domain):
    """
    기본 질의문
    """
    query: str


@dataclass
class ElasticSearchDomain(QueryDomain):
    """
    엘라스틱서치 검색을 위한 데이터 클래스
    """
    query_vector: List
    noun_tokens: List
    verb_tokens: List



@dataclass
class ElasticIndexDomain(Domain):
    """
    엘라스틱서치에 insert하기 위한 클래스
    """
    content_vector: List
    title: str
    first_header: str
    second_header: str
    content: str
    content_noun_tokens: List
    content_verb_tokens: List


@dataclass
class MrcDomain(QueryDomain):
    """
    MRC에 질의하기 위한 데이터 클래스
    """
    search_string: str