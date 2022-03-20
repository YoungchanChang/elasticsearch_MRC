import logging

import traceback
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.controller.mrc_control import MRC
from app.domain.custome_error import WikiDataException
from app.domain.domain import WikiQuestionItem, WikiQuestionItemDTO
from app.infrastructure.database.elastic_repository import WikiSearch, ElasticContent

formatter = "%(asctime)s.%(msecs)03d\t%(levelname)s\t[%(name)s]\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter, datefmt='%m/%d/%Y %I:%M:%S')

MRC_ANSWER = 0

router = APIRouter(
    prefix="/mrc",
    tags=["mrc_question"],
    responses={404: {"description": "Not found"}},
)


@router.post("/wiki_question")
async def find_data(wiki_question_item: WikiQuestionItem):
    mrc = MRC()

    try:

        mrc_answer, best_proper_content = mrc.filter_mrc_content(wiki_question_item.question)

        return_json = {"mrc_answer": mrc_answer,
                       "best_proper_content": best_proper_content,}

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


@router.post("/wiki_insert")
async def insert_data(wiki_question_item: WikiQuestionItem):

    try:

        result = ElasticContent().create(WikiQuestionItemDTO(title=wiki_question_item.question, question=None))
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