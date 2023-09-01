from typing import Iterable

import pytest

from chemchef.clients.openai.embeddings_client import OpenAIEmbedder
import numpy as np


def run_embedding_example(
        target_word: str,
        candidate_words: Iterable[str],
        rankings_thresholds: dict[str, int]
) -> None:
    """
    :param rankings_thresholds: {candidate word: ranking position threshold}
       The actual ranking position for a candidate word must be less than or equal to the ranking position for the
       test to pass. The numbering starts at 1.
    """
    embedder = OpenAIEmbedder()
    candidates_to_distances_from_target: dict[str, float] = {
        candidate_word: np.linalg.norm(embedder.embed(target_word) - embedder.embed(candidate_word))  # type: ignore
        for candidate_word in candidate_words
    }

    candidates_in_relevance_order: list[str] = sorted(
        candidate_words,
        key=candidates_to_distances_from_target.get  # type: ignore
    )
    for candidate_word in candidates_in_relevance_order:
        print("Candidate: {}, Distance = {:.3f}".format(  # type: ignore
            candidate_word, candidates_to_distances_from_target.get(candidate_word)))

    for word, ranking_threshold in rankings_thresholds.items():
        actual_ranking = candidates_in_relevance_order.index(word) + 1
        assert actual_ranking <= ranking_threshold


def test_simple_example() -> None:
    # This example is very intuitive.
    run_embedding_example(
        target_word = "beef",
        candidate_words = ["beef mince", "chicken", "carrot", "recipe", "book", "house"],
        rankings_thresholds={"beef mince": 1, "chicken": 2, "carrot": 3, "recipe": 4}
    )


def test_with_antonyms() -> None:
    # It's counter-intuitive that some antonyms are deemed closer than words about entirely different subjects!
    run_embedding_example(
        target_word = "modern",
        candidate_words = ["new-build", "furnished", "traditional", "affordable"],
        rankings_thresholds={"new-build": 2, "traditional": 2}
    )


def test_with_nonequivalent_words_about_same_subject() -> None:
    run_embedding_example(
        target_word = "football",
        candidate_words = ["Lionel Messi", "referee", "sport", "Magnus Carlsen", "Gordon Ramsay"],
        rankings_thresholds={"Lionel Messi": 3, "referee": 3, "sport": 3}
    )


def test_with_number_differences() -> None:
    run_embedding_example(
        target_word = "cat",
        candidate_words = ["cats", "dog"],
        rankings_thresholds={"cats": 1}
    )


def test_with_tense_differences() -> None:
    run_embedding_example(
        target_word = "come",
        candidate_words = ["came", "coming", "go", "went", "gone"],
        rankings_thresholds={"came": 2, "coming": 2}
    )


def test_with_compound_concept() -> None:
    run_embedding_example(
        target_word = "lamb korma",
        candidate_words = ["lamb korma", "mutton korma", "chicken korma", "lamb vindaloo", "lamb tagine", "chicken tagine"],
        rankings_thresholds={"lamb korma": 1, "mutton korma": 2, "lamb vindaloo": 5}
    )
