from abc import ABC, abstractmethod
from typing import Iterable, NamedTuple
import logging

from chemchef.clients.openai import OpenAIChatHandler, ChatMessage, SystemMessage, UserMessage, AssistantMessage


class AbstractKeywordSimilarityTest(ABC):
    """A method for testing whether different words have similar meanings. Useful for fuzzy lookups on an index."""

    @abstractmethod
    def find_matches(self, target_keyword: str, candidate_keywords: Iterable[str]) -> set[str]:
        """
        :param target_keyword: the target keyword
        :param candidate_keywords: a list or set of candidate keywords that may or may not be
            similar to the target keyword
        :return: a set containing the candidate keywords that are deemed to match the target keyword
        """
        raise NotImplementedError


SYSTEM_MESSAGE = "Given a target phrase and a list of candidate phrases, "\
                 "the AI assistant determines which of the candidate phrases are "\
                 "synonyms, hyponyms or hypernyms of the target phrase. "\
                 "Note that phrases are deemed to match if they differ in tense or number."

USER_MESSAGE_TEMPLATE = "Target: {}\nCandidates: {}"

ASSISTANT_MESSAGE_TEMPLATE = "Synonyms: {}\nHyponyms: {}\nHypernyms: {}"


class TargetCandidatesTuple(NamedTuple):
    target: str
    candidates: Iterable[str]


class SynonymsHyponymsHypernymsTuple(NamedTuple):
    synonyms: set[str]
    hyponyms: set[str]
    hypernyms: set[str]


class SimilarityTaskExample(NamedTuple):
    target: str
    candidates: Iterable[str]
    synonyms: set[str]
    hyponyms: set[str]
    hypernyms: set[str]

    @property
    def target_and_candidates(self) -> TargetCandidatesTuple:
        return TargetCandidatesTuple(target=self.target, candidates=self.candidates)

    @property
    def synonyms_hyponyms_hypernyms(self) -> SynonymsHyponymsHypernymsTuple:
        return SynonymsHyponymsHypernymsTuple(
            synonyms=self.synonyms, hyponyms=self.hyponyms, hypernyms=self.hypernyms)


class SimilarityTestResponseParsingError(Exception):
    pass


def construct_user_message(target_candidates_tuple: TargetCandidatesTuple) -> str:
    return USER_MESSAGE_TEMPLATE.format(
        target_candidates_tuple.target,
        ', '.join(target_candidates_tuple.candidates)
    )


def construct_assistant_message(synonyms_hyponyms_hypernyms_tuple: SynonymsHyponymsHypernymsTuple) -> str:
    return ASSISTANT_MESSAGE_TEMPLATE.format(
        ', '.join(synonyms_hyponyms_hypernyms_tuple.synonyms),
        ', '.join(synonyms_hyponyms_hypernyms_tuple.hyponyms),
        ', '.join(synonyms_hyponyms_hypernyms_tuple.hypernyms)
    )


def parse_assistant_message(message_contents: str, candidates: Iterable[str]) -> SynonymsHyponymsHypernymsTuple:
    lines: list[str] = [line.strip() for line in message_contents.strip().splitlines()]
    if (not len(lines) == 3 or
            not(lines[0].startswith("Synonyms:")
                and lines[1].startswith("Hyponyms:")
                and lines[2].startswith("Hypernyms:"))):
        raise SimilarityTestResponseParsingError(f"Cannot parse chat response: {message_contents}")

    comma_separated_synonyms = lines[0][len("Synonyms:"):].strip()
    comma_separated_hyponyms = lines[1][len("Hyponyms:"):].strip()
    comma_separated_hypernyms = lines[2][len("Hypernyms:"):].strip()

    synonyms = set(word.strip() for word in comma_separated_synonyms.split(", ") if len(word.strip()) > 0)
    hyponyms = set(word.strip() for word in comma_separated_hyponyms.split(", ") if len(word.strip()) > 0)
    hypernyms = set(word.strip() for word in comma_separated_hypernyms.split(", ") if len(word.strip()) > 0)

    if len(synonyms.difference(candidates)) > 0:
        raise SimilarityTestResponseParsingError(
            f"Synonyms in chat response are not among the original candidates: {synonyms.difference(candidates)}")
    if len(hyponyms.difference(candidates)) > 0:
        raise SimilarityTestResponseParsingError(
            f"Hyponyms in chat response are not among the original candidates: {hyponyms.difference(candidates)}")
    if len(hypernyms.difference(candidates)):
        raise SimilarityTestResponseParsingError(
            f"Hypernyms in chat response are not among the original candidates: {hypernyms.difference(candidates)}")

    return SynonymsHyponymsHypernymsTuple(synonyms=synonyms, hyponyms=hyponyms, hypernyms=hypernyms)


EXAMPLES: list[SimilarityTaskExample] = [
    SimilarityTaskExample(
        target="house",
        candidates=["ocean", "building", "home", "cottage", "bus", "mansion", "table"],
        synonyms={"building"},
        hyponyms={"home", "cottage", "mansion"},
        hypernyms=set()
    ),
    SimilarityTaskExample(
        target="cottage",
        candidates=["farmhouse", "palace", "house"],
        synonyms={"farmhouse"},
        hyponyms=set(),
        hypernyms={"house"}
    ),
    SimilarityTaskExample(
        target="happy",
        candidates=["overjoyed", "gleeful", "downcast", "morose", "emotional"],
        synonyms={"overjoyed", "gleeful"},
        hyponyms=set(),
        hypernyms={"emotional"}
    ),
    SimilarityTaskExample(
        target="give up",
        candidates=["quit", "persevere", "stop trying", "carry on", "throw the towel in", "watch TV"],
        synonyms={"quit", "stop trying", "throw the towel in"},
        hyponyms=set(),
        hypernyms=set()
    ),
    SimilarityTaskExample(
        target="egg",
        candidates=["egg", "EGG", "eggs", "fish", "ostrich eggs"],  # same word, capitalised word, plural form of word
        synonyms={"egg", "EGG", "eggs"},
        hyponyms={"ostrich eggs"},
        hypernyms=set()
    ),
    SimilarityTaskExample(
        target="run",
        candidates=["ran", "runs", "running", "cycling", "cycle"],  # different forms of the verb
        synonyms={"ran", "runs", "running"},
        hyponyms=set(),
        hypernyms=set()
    ),
    SimilarityTaskExample(
        target="country",
        candidates=["UK", "USA", "slcxzlwoei"],  # candidate is not a real word
        synonyms=set(),
        hyponyms={"UK", "USA"},
        hypernyms=set()
    ),
    SimilarityTaskExample(
        target="mfpkfwkd",  # target is not a real word
        candidates=["apple"],
        synonyms=set(),
        hyponyms=set(),
        hypernyms=set()
    )
]


class OpenAIKeywordSimilarityTest(AbstractKeywordSimilarityTest):
    """
    Uses OpenAI to determine matches.
    Note that synonyms and hyponyms are considered to be matches, but hypernyms are not.
    """

    def __init__(self) -> None:
        self._chat_handler = OpenAIChatHandler()

    def find_matches(self, target_keyword: str, candidate_keywords: Iterable[str]) -> set[str]:
        prompt = self._construct_prompt(target_keyword, candidate_keywords)
        response = self._chat_handler.run(prompt)
        response_tuple = self._parse_response(response, candidate_keywords)

        # Include synonyms and hyponyms but NOT hypernyms.
        matches: set[str] = set()
        matches.update(response_tuple.synonyms)
        matches.update(response_tuple.hyponyms)

        # If there is an exact match, then make sure to include it. (ChatGPT sometimes doesn't consider exact matches to be synonyms.)
        if target_keyword in candidate_keywords:
            matches.add(target_keyword)

        return matches

    @staticmethod
    def _construct_prompt(target: str, candidates: Iterable[str]) -> list[ChatMessage]:
        messages: list[ChatMessage] = []

        messages.append(
            SystemMessage(content=SYSTEM_MESSAGE))

        for example in EXAMPLES:
            messages.append(
                UserMessage(content=construct_user_message(example.target_and_candidates)))
            messages.append(
                AssistantMessage(content=construct_assistant_message(example.synonyms_hyponyms_hypernyms)))

        current_target_and_candidates = TargetCandidatesTuple(target=target, candidates=candidates)
        messages.append(
            UserMessage(content=construct_user_message(current_target_and_candidates)))

        return messages

    @staticmethod
    def _parse_response(response: AssistantMessage, candidates: Iterable[str]) -> SynonymsHyponymsHypernymsTuple:
        logging.debug("Response from ChatGPT for similarity test: %s", response.content)
        return parse_assistant_message(response.content, candidates)
