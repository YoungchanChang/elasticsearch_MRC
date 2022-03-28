from typing import List, Optional

from attr import dataclass


@dataclass
class ElasticParsingResult:
    """엘라스틱서치 파싱 결과값"""
    score: int
    title: str
    first_header: str
    second_header: str
    content: str
    content_noun_tokens: Optional[List]
    content_verb_tokens: Optional[List]
    content_match_tokens: Optional[List]


@dataclass
class ElasticFieldDto:
    """엘라스틱서치 필드 값 설정 도메인"""
    title: str
    first_header: str
    second_header: str
    content: str
    content_vector: List
    content_noun_tokens: List
    content_verb_tokens: List
