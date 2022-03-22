from app.application.repo_interface import AbstractRepository, AbstractFinder
from app.application.mecab_service import filter_necessary
from app.domain.domain import WikiQuestionItemDTO


class ElasticService:

    def __init__(self, finder: AbstractFinder, repository: AbstractRepository):
        self.finder = finder
        self.repository = repository

    def get_content(self, question: str):
        wiki_question = WikiQuestionItemDTO(title=None,question=question)
        title = self.finder.find_one(model=wiki_question)

        question = filter_necessary(question.replace(title, ""))
        wiki_question = WikiQuestionItemDTO(title=title, question=question)
        content = self.repository.find_one(model=wiki_question)

        return content