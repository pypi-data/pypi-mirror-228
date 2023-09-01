from typing import Iterable

from chemchef.clients.internet.google import SearchResult
from chemchef.clients.openai import OpenAIChatHandler, ChatMessage, SystemMessage, UserMessage

SYSTEM_MESSAGE = "The human user is using Google search in order to answer a question. "\
                 "The AI assistant is advising the human user on how to get the most out of Google search.\n\n"\
                 "CONVERSATION FORMAT:\n\n"\
                 "User message:\n"\
                 "Search query string: [A search query that the user has just typed into Google]\n"\
                 "Search results: [A bullet point list of the results returned by this search]\n\n"\
                 "AI response:\n"\
                 "Likely purpose of search: [A guess as to what the user is trying to accomplish from this search,]\n"\
                 "Criticism of search results: [One or two sentences on whether any of the search results are "\
                 "particularly unlikely to contain the information required, or whether "\
                 "any of the search search results are particularly unreliable as sources of information. "\
                 "Example: 'The first search result explains how the iPhone 11 has a longer battery life than "\
                 "other smartphones, whereas the intent is to discover smartphones with longer battery life than "\
                 "the iPhone.']\n"\
                 "Criticism of search query string: [One or two sentences on whether the search query string "\
                 "is likely to be effective for achieving the intended purpose, and "\
                 "an example of a more effective Google search query (if appropriate). "\
                 "Often, a search query that directly describes ones' intent is ineffective, since it is unlikely "\
                 "that anyone has created a web page addressing the specific problem that one is trying to address now. "\
                 "In these situations, a more indirect or roundabout search query might be more effective. "\
                 "It might even be more effective to break up the problem into two or more less specific search queries. "\
                 "This is the kind of feedback that should be provided in these one or two sentences of feedback. "\
                 "Example: 'Searching for 'Donald Trump Bill Clinton age difference' is unlikely to yield useful "\
                 "results, since it is unlikely that anyone will have created a web page that specifically states the "\
                 "age difference between these two politicians. Also, reliable web pages are more likely to provide "\
                 "dates of birth, since a person's age changes from year to year. Consider searching for "\
                 "'Donald Trump date of birth' and 'Bill Clinton date of birth' separately'.]\n\n"\
                 "WARNING:\n\nAt no point should the AI assistant mention 'the user' in its response. When talking "\
                 "about the user's intent, the AI should refer to 'the intent of the search'."

USER_MESSAGE_TEMPLATE = "Search query string: {}\nSearch results:\n{}"


def _construct_user_message(query_string: str, search_results: list[SearchResult]) -> str:
    search_results_list = '\n'.join('- ' + str(result) for result in search_results)
    return USER_MESSAGE_TEMPLATE.format(query_string, search_results_list)


def _parse_assistant_message(message: str) -> str:
    lines = [line.strip() for line in message.splitlines()
             if len(line.strip()) > 0 and not line.startswith("Likely purpose of search: ")]
    return '\n'.join(lines)


def critique_search_results(query_string: str, search_results: list[SearchResult]) -> str:
    handler = OpenAIChatHandler()

    prompts: list[ChatMessage] = [
        SystemMessage(content=SYSTEM_MESSAGE),
        UserMessage(content=_construct_user_message(query_string, search_results))
    ]

    response = handler.run(prompts)

    return _parse_assistant_message(response.content)
