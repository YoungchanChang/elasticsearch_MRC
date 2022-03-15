from dataclasses import dataclass

@dataclass
class WikiItem:
    title: str
    first_header: str
    second_header: str
    content: str
