import pytest

from app.domain.custome_error import WikiDataException
from app.domain.domain import WikiQuestionItemDTO
from app.infrastructure.database.elastic_repository import WikiSearch


def test_():
    wiki_question = WikiQuestionItemDTO(title="조선", question="조선 최고 학당이 어디야?")
    wiki_search = WikiSearch()
    wiki_result = wiki_search.find_one(wiki_question)

    assert len(wiki_result.body['hits']['hits']) > 0

    with pytest.raises(WikiDataException):
        wiki_question = WikiQuestionItemDTO(title="조선ㅇ", question="조선 최고 학당이 어디야?")
        wiki_search.find_one(wiki_question)


