import logging

import traceback
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.controller.mrc_control import MRC
from app.domain.custome_error import WikiDataException
from app.domain.domain import WikiQuestionItem, WikiQuestionItemDTO
from app.infrastructure.database.elastic_repository import WikiSearch

formatter = "%(asctime)s.%(msecs)03d\t%(levelname)s\t[%(name)s]\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter, datefmt='%m/%d/%Y %I:%M:%S')

MRC_ANSWER = 0

router = APIRouter(
    prefix="/mrc",
    tags=["mrc_question"],
    responses={404: {"description": "Not found"}},
)


@router.post("/wiki_question")
async def create_index(wiki_question_item: WikiQuestionItem):
    mrc = MRC()
    wiki_search = WikiSearch()

    try:
        wiki_answer = wiki_search.find_one(WikiQuestionItemDTO(title=wiki_question_item.title, question=wiki_question_item.question))

        if not wiki_answer:
            raise Exception

        result = mrc.get_pororo_answer(wiki_question_item.question)
        return_json = {"result": result[MRC_ANSWER]}
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
