from typing import Optional

import pytest

from chemchef.engine.generation.generation import OpenAIDocumentGenerator, DocumentGenerationError


def run_example(subject: str,
                format: str,
                expected_contents: list[str],
                must_have_all: Optional[set[str]] = None,
                must_have_at_least_one: Optional[set[str]] = None,
                should_fail: bool = False) -> None:
    """
    :param must_have_all: The text generated must contain all of these words for the test to pass
    :param must_have_at_least_one: The text generated must contain at least one of these words for the test to pass
    :param should_fail: If true, the generation is expected to fail, e.g. due to a logically invalid subject being provided
    :return:
    """
    print(f"Subject: {subject}\nFormat: {format}\nExpected contents = {expected_contents}")

    generator = OpenAIDocumentGenerator()

    generated_doc = generator.generate(subject, format, expected_contents)

    if generated_doc is not None:
        print(f"\n{generated_doc}")

        doc_length = len(generated_doc.split())
        assert 10 <= doc_length <= 200

        actual_words = {_clean_word(word) for word in generated_doc.split()}
        if must_have_all:
            assert all(_clean_word(word) in actual_words for word in must_have_all)
        if must_have_at_least_one:
            assert any(_clean_word(word) in actual_words for word in must_have_at_least_one)

        assert not should_fail
    else:
        print('No document generated: subject and format deemed incompatible')
        assert should_fail


def _clean_word(word: str) -> str:
    lower_case_word = word.lower()
    word_with_alphanumerics_only = ''.join(char for char in lower_case_word if char.isalnum())
    return word_with_alphanumerics_only


@pytest.mark.flaky(reruns=3)
def test_simple_case() -> None:
    run_example(
        subject="London",
        format="Travel guide",  # occasionally generates instructions for tourists rather than facts about the city
        expected_contents=["Historical landmarks", "Museums"],
        must_have_all={"Museum"},  # e.g. British Museum, Natural History Museum
        must_have_at_least_one={"Tower", "Ben", "Westminster", "Parliament"}  # i.e. Tower of London, Big Ben...
    )


@pytest.mark.flaky(reruns=3)
def test_simple_case_v2() -> None:
    run_example(
        subject="Chicken korma",
        format="Recipe",  # sometimes displays ingredients as bullet-point list, sometimes doesn't
        expected_contents=["Ingredients", "Cooking time"],
        must_have_all={"minutes", "garlic", "ginger"}  # any reasonable curry recipe would include garlic and ginger
    )


@pytest.mark.flaky(reruns=3)
def test_with_nonexistent_subject() -> None:
    run_example(
        subject="Nick Dorey",  # not famous enough to be in the training set
        format="Politician biography",
        expected_contents=["Date of birth", "Known for"],
        should_fail=True
    )


@pytest.mark.flaky(reruns=3)
def test_with_subject_who_doesnt_fit_description() -> None:
    run_example(
        subject="Ricky Gervais",  # not a politician
        format="Politician biography",
        expected_contents=["Date of birth", "Known for"],
        should_fail=True
    )
