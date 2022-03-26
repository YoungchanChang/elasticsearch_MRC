# from dataclasses import dataclass
# from typing import Optional
#
# from pydantic import BaseModel
#
#
# @dataclass
# class Domain:
#     ...
#
#
# @dataclass
# class WikiTitle(Domain):
#     title: str
#
#
# @dataclass
# class WikiItem(WikiTitle):
#     first_header: str
#     second_header: str
#     content: str
#
#
#
# @dataclass
# class WikiQuestionItemDTO(Domain):
#     title: Optional[str]
#     question: Optional[str]
#
#
# class WikiQuestionItem(BaseModel):
#     question: str
#
#
