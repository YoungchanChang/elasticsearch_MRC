# from app.application.repo_interface import AbstractFinder
# from app.domain.domain import WikiQuestionItemDTO
#
#
# class WikipediaService:
#
#     def __init__(self, repository: AbstractFinder):
#         self.repository = repository
#
#     def get_wiki_data(self, title: str):
#         wiki_question = WikiQuestionItemDTO(title=title,question=None)
#         wiki_data = self.repository.find_one(model=wiki_question)
#         return wiki_data
#
#
