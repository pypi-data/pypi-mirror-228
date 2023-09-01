from typing import Iterable

from googlesearch import search  # type: ignore
from pydantic import BaseModel


class SearchResult(BaseModel):
    url: str
    title: str
    description: str

    def __repr__(self) -> str:
        return f"url={self.url}, title={self.title}, description={self.description}"

    def __str__(self) -> str:
        return repr(self)


def google_search(query: str, max_results: int = 10) -> list[SearchResult]:
    results = search(query, num_results=max_results, advanced=True)

    parsed_results = [SearchResult(url=result.url, title=result.title, description=result.description)
                      for result in results]

    if len(parsed_results) > max_results:
        parsed_results = parsed_results[:max_results]

    return parsed_results
