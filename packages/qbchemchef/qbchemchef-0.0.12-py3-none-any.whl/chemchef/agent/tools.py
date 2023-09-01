from abc import ABC, abstractmethod
from typing import Iterable

from chemchef.agent.search_critique.search_critique import critique_search_results
from chemchef.agent.summarization import summarise
from chemchef.clients.internet import load_page, PageLoadingError
from chemchef.clients.internet.google import SearchResult, google_search


class ToolUsageError(Exception):
    pass


class AbstractTool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def input_format_description(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def run(self, input_text: str) -> str:
        raise NotImplementedError


class GoogleSearchTool(AbstractTool):
    NAME = "Google Search"

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def description(self) -> str:
        return "Given a search query string, returns a list of URLs obtained by a running a Google search with this query string, "\
               "plus some comments from the user on how effective the search seemed to be."

    @property
    def input_format_description(self) -> str:
        return "the search query string to enter into Google"

    def run(self, input_text: str) -> str:
        search_query = input_text
        search_results = google_search(search_query)

        criticism = critique_search_results(search_query, search_results)

        return self._format_search_results(search_results, criticism)

    @staticmethod
    def _format_search_results(search_results: list[SearchResult], criticism: str) -> str:
        return ('Results of google search:\n' + '\n'.join('- ' + str(result) for result in search_results)
                + '\n\n' + criticism)


class QuestionAnsweringFromWebPageTool(AbstractTool):
    NAME = "Question Answering From Web Page"

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def description(self) -> str:
        return "Given a question followed by a URL of a web page, "\
               "returns an answer to the question extracted from the information in the web page."

    @property
    def input_format_description(self) -> str:
        return "the question, followed by the URL, separated by a space"

    def run(self, input_text: str) -> str:
        question, url = self._parse_input(input_text)

        try:
            web_page_text = load_page(url)
        except PageLoadingError as ex:
            return self._format_error_output(str(ex))

        answer = summarise(question, web_page_text)
        return self._format_answer_output(answer)

    @staticmethod
    def _parse_input(input_text: str) -> tuple[str, str]:
        words = [word for word in input_text.split()
                 if not word.lower().startswith('question') and not word.lower().startswith('url')]

        if len(words) < 2:
            raise ToolUsageError("The input to this tool should contain a question followed by a URL.")

        question = ' '.join(words[:-1]).strip()
        url = words[-1]

        if question[-1] != '?':
            raise ToolUsageError("The input to this tool should start with a question.")

        if 'http' not in url:
            raise ToolUsageError("The input to this tool should end with a URL (containing the scheme http or https).")

        return question, url

    @staticmethod
    def _format_answer_output(answer: str) -> str:
        return answer  # the answer already has headers (e.g. "Answer", "Criticism...")

    @staticmethod
    def _format_error_output(error: str) -> str:
        return f"ERROR: {error}"


STANDARD_TOOLS: list[AbstractTool] = [
    GoogleSearchTool(),
    QuestionAnsweringFromWebPageTool()
]
