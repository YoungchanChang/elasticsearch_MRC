# from app.application.repo_interface import AbstractRepository, AbstractFinder
# from app.application.mecab_service import filter_necessary, MecabInflectParser
# from app.domain.domain import WikiQuestionItemDTO
#
#
# class ElasticService:
#
#     def __init__(self, finder: AbstractFinder, repository: AbstractRepository):
#         self.finder = finder
#         self.repository = repository
#
#     def get_content(self, question: str):
#
#         """
#         제목을 가져온 뒤, 제목 기준으로 데이터를 추출하는 기능
#         :param question: 질의문
#         :return: 질의문에서 엘라스틱서치에서 가져온 답변
#         """
#
#         wiki_question = WikiQuestionItemDTO(title=None,question=question)
#         title = self.finder.find_one(model=wiki_question)
#
#         question = " ".join([x[0] for x in list(MecabInflectParser(question.replace(title, "")).gen_mecab_compound_token_feature())])
#         wiki_question = WikiQuestionItemDTO(title=title, question=question)
#         content = self.repository.find_one(model=wiki_question)
#
#         return content