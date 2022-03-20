from app.application.repo_interface import AbstractRepository, AbstractFinder
from app.domain.custome_error import WikiDataException
from app.domain.domain import Domain, WikiQuestionItemDTO
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('ko')


class WikiContent(AbstractFinder):

    def find_one(self, model: WikiQuestionItemDTO):
        page_py = wiki_wiki.page(model.title)

        if page_py.text == '':
            raise WikiDataException("위키피디아 데이터 없음")
        return page_py