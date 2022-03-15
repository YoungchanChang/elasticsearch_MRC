from typing import Generator

import wikipediaapi
from domain.domain_data import WikiItem
from kss import split_sentences

wiki_wiki = wikipediaapi.Wikipedia('ko')


def get_wiki_data(keyword: str) -> Generator:

    page_py = wiki_wiki.page(keyword)

    for page_item in split_sentences(page_py.summary):
        yield WikiItem(title=page_py.title,
                       first_header="summary",
                       second_header="summary",
                       content=page_item)

    for page_section in page_py.sections:
        for page_sec_item in page_section.sections:

            for page_test_item in page_sec_item.text.split("\n"):
                if page_test_item == "" or page_test_item == "\t\t":
                    continue
                yield WikiItem(title=page_py.title,
                               first_header=page_section.title,
                               second_header=page_sec_item.title,
                               content=page_test_item)


if __name__ == "__main__":
    for i in get_wiki_data("조선"):
        print(i)