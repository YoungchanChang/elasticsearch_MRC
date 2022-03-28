import logging
import traceback

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.controller.adapter.elastic_dto import ElasticFieldDto
from app.controller.adapter.fastapi_dto import WikiQuestionItem, ElasticIndexItem
from app.controller.adapter.wiki_dto import WikiTitle
from app.controller.error_handler.custom_error import WikiDataException
from app.domain.entity import QueryDomain
from app.infrastructure.api.wiki_repo import WikipediaRepository
from app.infrastructure.database.elastic_repository import ElasticRepository
from app.infrastructure.nlp_model.nlp import ElasticMrc, PororoMecab

formatter = "%(asctime)s.%(msecs)03d\t%(levelname)s\t[%(name)s]\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter, datefmt='%m/%d/%Y %I:%M:%S')

MRC_FILTER_SENTENCE = 2

router = APIRouter(
    prefix="/mrc",
    tags=["mrc_question"],
    responses={404: {"description": "Not found"}},
)


@router.post("/search_sentence")
async def find_data(wiki_question_item: WikiQuestionItem):
    elastic_mrc = ElasticMrc()

    try:

        elastic_content = elastic_mrc.get_content(question=wiki_question_item.question)
        mrc_filtered_content = elastic_mrc.get_mrc_content(question=wiki_question_item.question, elastic_contents=elastic_content)

        return_json = {"best_proper_sentence": mrc_filtered_content[MRC_FILTER_SENTENCE]}

        return jsonable_encoder(return_json)

    except WikiDataException as wde:
        return_json = {"result": "위키피디아에 없는 주제입니다."}
        logging.critical({'status': 'fail', "message": wde})
        return jsonable_encoder(return_json)

    except Exception as e:
        error_msg = traceback.format_exc()
        logging.critical({'status': 'fail', "message": error_msg})
        return_json = {"result": "서버에 문제가 생겼습니다. 관리자에게 문의하세요."}
        return jsonable_encoder(return_json)


@router.post("/insert_document")
async def insert_data(elastic_index: ElasticIndexItem):
    pororo_nlp = PororoMecab()
    es_repo = ElasticRepository()
    try:
        _query = QueryDomain(query=elastic_index.title)
        embedding_vectors = pororo_nlp.get_embeddings(domain=_query)
        nouns, verbs = pororo_nlp.get_nouns_verbs(domain=QueryDomain(query=elastic_index.content))
        nouns = list(set(list(nouns)))
        verbs = list(set(list(verbs)))
        elastic_index_domain = ElasticFieldDto(content_vector=embedding_vectors,
                                               title=elastic_index.title,
                                               first_header=elastic_index.first_header,
                                               second_header=elastic_index.second_header,
                                               content=elastic_index.content,
                                               content_noun_tokens=nouns,
                                               content_verb_tokens=verbs)
        result = es_repo.create(elastic_index_domain)

        return_json = {"result": result}

        return jsonable_encoder(return_json)

    except Exception as e:
        error_msg = traceback.format_exc()
        logging.critical({'status': 'fail', "message": error_msg})
        return_json = {"result": "서버에 문제가 생겼습니다. 관리자에게 문의하세요."}
        return jsonable_encoder(return_json)


@router.post("/insert_wiki_subject")
async def insert_wiki_data(wiki_question_item: WikiQuestionItem):

    try:
        pororo_mecab = PororoMecab()
        wiki_repo = WikipediaRepository(nlp_model=pororo_mecab)
        wiki_title = WikiTitle(title=wiki_question_item.question)
        result = wiki_repo.create(domain=wiki_title)
        return_json = {"result": result}

        return jsonable_encoder(return_json)

    except WikiDataException as wde:
        return_json = {"result": "위키피디아에 없는 주제입니다."}
        logging.critical({'status': 'fail', "message": wde})
        return jsonable_encoder(return_json)

    except Exception as e:
        error_msg = traceback.format_exc()
        logging.critical({'status': 'fail', "message": error_msg})
        return_json = {"result": "서버에 문제가 생겼습니다. 관리자에게 문의하세요."}
        return jsonable_encoder(return_json)