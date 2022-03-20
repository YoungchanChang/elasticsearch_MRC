import mecab

from app.application.repo_interface import AbstractRepository, AbstractFinder
from app.domain.domain import WikiQuestionItemDTO

mecab = mecab.MeCab()


mecab_pos_allow = [
                "NNG", "NNP", "NR",
                "VV", "VA", "VX",
                "XPN", "XSN", "XSV", "XSA", "XR",
                "MM",
                "SL", "SH", "SN",]


def filter_necessary(question: str) -> str:
    mecab_parsed = mecab.parse(question)
    answer = []
    for i in mecab_parsed:
        i_post = i[1].pos.split("+")
        if any(elem in i_post for elem in mecab_pos_allow):
            answer.append(i[0])

    return " ".join(answer)


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