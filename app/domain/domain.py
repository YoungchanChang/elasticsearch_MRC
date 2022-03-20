from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

@dataclass
class Domain:
    ...

@dataclass
class WikiItem(Domain):
    title: str
    first_header: str
    second_header: str
    content: str



@dataclass
class WikiQuestionItemDTO(Domain):
    title: Optional[str]
    question: Optional[str]


class WikiQuestionItem(BaseModel):
    title: str
    question: str


