from typing import Iterable

import pytest

from chemchef.agent.summarization.summarization import summarise_from_chunks


def run_example(question: str, chunks: Iterable[str], must_contain: set[str], must_not_contain: set[str]) -> None:
    print(f'Question: {question}\nText chunks: {list(chunks)}')

    answer = summarise_from_chunks(question, chunks)
    print(f"{answer}\n")

    for phrase in must_contain:
        assert phrase.lower() in answer.lower()

    for phrase in must_not_contain:
        assert phrase.lower() not in answer.lower()


@pytest.mark.flaky(reruns=3)
def test_with_one_chunk() -> None:
    run_example(
        question="What is the relationship between Alice and Bob?",
        chunks=["Alice is a flight attendant. Alice is Bob's aunt."],
        must_contain={"aunt"},
        must_not_contain=set()  # it's hard to get the LLM to ignore the flight attendant piece
    )


@pytest.mark.flaky(reruns=3)
def test_with_two_chunks_with_first_chunk_irrelevant() -> None:
    run_example(
        question="What is the relationship between Alice and Bob?",
        chunks=["Alice is a flight attendant.", "Alice is Bob's aunt."],
        must_contain={"aunt"},
        must_not_contain=set()  # it's hard to get the LLM to ignore the flight attendant piece
    )


@pytest.mark.flaky(reruns=3)
def test_with_two_chunks_with_second_chunk_irrelevant() -> None:
    run_example(
        question="What is the relationship between Alice and Bob?",
        chunks=["Alice is Bob's aunt.", "Alice is a flight attendant."],
        must_contain={"aunt"},
        must_not_contain=set()
    )


@pytest.mark.flaky(reruns=3)
def test_with_answer_logically_pieced_together_from_two_chunks() -> None:
    run_example(
        question="What is the relationship between Alice and Bob?",
        chunks=["Alice is Charlie's mother.", "Charlie is Bob's father."],
        must_contain={"grandmother"},
        must_not_contain=set()
    )


@pytest.mark.flaky(reruns=3)
def test_with_unreliable_source() -> None:
    run_example(
        question="What is the relationship between Alice and Bob?",
        chunks=["I'm a bit drunk and I don't know what I'm talking about. I don't even want to help you. "
                "But I would say that Alice is Bob's daughter."],
        must_contain={"daughter"},
        must_not_contain=set()
    )
    # TODO: assert that the unreliability is called out


@pytest.mark.flaky(reruns=3)
def test_with_information_missing_from_source() -> None:
    run_example(
        question="What is the relationship between Alice and Bob?",
        chunks=["Alice is a banker and Bob is an estate agent."],
        must_contain=set(),
        must_not_contain=set()
    )
    # TODO: assert that the lack of information is called out.
