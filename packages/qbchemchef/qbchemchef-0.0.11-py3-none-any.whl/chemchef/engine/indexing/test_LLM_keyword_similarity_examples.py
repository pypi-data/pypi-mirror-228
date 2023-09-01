from typing import Iterable, Optional

import pytest

from chemchef.engine.indexing.keyword_similarity import OpenAIKeywordSimilarityTest, SimilarityTestResponseParsingError


def run_example(target_keyword: str,
                candidate_keywords: Iterable[str],
                must_match: Optional[Iterable[str]] = None,
                must_not_match: Optional[Iterable[str]] = None) -> None:
    print(f"Target keyword: {target_keyword}\nCandidate keywords: {', '.join(candidate_keywords)}")
    similarity_test = OpenAIKeywordSimilarityTest()
    results = similarity_test.find_matches(target_keyword, candidate_keywords)
    print(f"Matches: {', '.join(results)}")

    if must_match:
        false_negatives = {word for word in must_match if word not in results}
        assert len(false_negatives) == 0
    if must_not_match:
        false_positives = {word for word in must_not_match if word in results}
        assert len(false_positives) == 0


@pytest.mark.flaky(reruns=3)
def test_simple_case() -> None:
    run_example(
        target_keyword="beef",
        candidate_keywords=["beef mince", "chicken", "carrot", "recipe", "book", "house"],
        must_match=["beef mince"],
        must_not_match=["chicken", "carrot", "recipe", "book", "house"]
    )


@pytest.mark.flaky(reruns=3)
def test_with_compound_concept() -> None:
    run_example(
        target_keyword="lamb curry",
        candidate_keywords=["lamb korma", "chicken curry", "lamb tagine", "lamb chops"],  # sometimes the LLM thinks a tagine is a curry
        must_match=["lamb korma"],
        must_not_match=["chicken curry", "lamb chops"]
    )


@pytest.mark.flaky(reruns=3)
def test_with_hyponyms() -> None:
    run_example(
        target_keyword="meat",
        candidate_keywords=["beef mince", "chicken", "carrot", "recipe", "book", "house"],
        must_match=["beef mince", "chicken"],
        must_not_match=["carrot", "recipe", "book", "house"]
    )


@pytest.mark.flaky(reruns=3)
def test_with_hypernyms_being_ignored() -> None:
    run_example(
        target_keyword="lamb",
        candidate_keywords=["mutton", "meat", "carrot"],  # "meat" is a hypernym of "lamb", so is ignored
        must_match=["mutton"],
        must_not_match=["meat", "carrot"]
    )


@pytest.mark.flaky(reruns=3)
def test_with_pluralizations() -> None:
    run_example(
        target_keyword="cat",
        candidate_keywords=["cat", "cats", "dog", "dogs", "kitten", "kittens"],  # pluralisation is accepted
        must_match=["cat", "cats", "kitten", "kittens"],
        must_not_match=["dog", "dogs"]
    )


@pytest.mark.flaky(reruns=3)
def test_with_tense_differences() -> None:
    run_example(
        target_keyword="come",
        candidate_keywords=["came", "went", "coming", "going", "being"],  # past tense etc are allowed
        must_match=["came", "coming"],
        must_not_match=["went", "going", "being"]
    )


@pytest.mark.flaky(reruns=3)
def test_with_science_knowledge() -> None:
    run_example(
        target_keyword="hydrophilic",
        candidate_keywords=["polar", "mixes with water", "soluble in hexane"],  # polar is debatable, but is usually returned
        must_match=["polar", "mixes with water"],
        must_not_match=["soluble in hexane"]
    )


@pytest.mark.flaky(reruns=3)
def test_with_science_knowledge_v2() -> None:
    run_example(
        target_keyword="ethanoic acid",
        candidate_keywords=["acetic acid", "vinegar", "acetone"],  # vinegar is debatable, but is usually returned
        must_match=["acetic acid", "vinegar"],
        must_not_match=["acetone"]
    )

