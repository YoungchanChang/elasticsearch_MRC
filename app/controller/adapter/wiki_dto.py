from dataclasses import dataclass


@dataclass
class WikiTitle:
    title: str


@dataclass
class WikiItem(WikiTitle):
    first_header: str
    second_header: str
    content: str
