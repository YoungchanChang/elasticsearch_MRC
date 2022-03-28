from pydantic import BaseModel


class WikiQuestionItem(BaseModel):
    question: str


class ElasticIndexItem(BaseModel):
    title: str
    first_header: str
    second_header: str
    content: str