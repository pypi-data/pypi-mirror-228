from typing import Any, Iterable

import pytest

from chemchef.clients.chroma.chroma_client import ChromaVectorCollection, ChromaVectorCollectionFactory
from chemchef.clients.openai.embeddings_client import AbstractEmbedder
import numpy as np

from chemchef.engine.extraction import ParsedDocument, ParsedField
from chemchef.engine.indexing.fuzzy_index import FuzzyIndex, FuzzyIndexCollection
from chemchef.engine.indexing.keyword_similarity import AbstractKeywordSimilarityTest


class DummyEmbedder(AbstractEmbedder):

    def embed(self, text: str) -> np.ndarray[np.float64, Any]:
        if text == 'foo':
            return np.array([1.0], dtype=np.float64)
        elif text == 'bar':
            return np.array([2.0], dtype=np.float64)
        else:
            return np.array([0.0], dtype=np.float64)


class ExactComparisonKeywordSimilarityTest(AbstractKeywordSimilarityTest):

    def find_matches(self, target_keyword: str, candidate_keywords: Iterable[str]) -> set[str]:
        return {
            keyword for keyword in candidate_keywords
            if keyword == target_keyword
        }


class FirstLetterComparisonKeywordSimilarityTest(AbstractKeywordSimilarityTest):

    def find_matches(self, target_keyword: str, candidate_keywords: Iterable[str]) -> set[str]:
        return {
            keyword for keyword in candidate_keywords
            if len(keyword) > 0 and len(target_keyword) > 0 and keyword[0] == target_keyword[0]
        }


class AlwaysTrueComparisonKeywordSimilarityTest(AbstractKeywordSimilarityTest):

    def find_matches(self, target_keyword: str, candidate_keywords: Iterable[str]) -> set[str]:
        return set(candidate_keywords)


def test_exact_query_when_results_found() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    index.add(0, {"x"})
    index.add(1, {"y", "z"})
    index.add(2, {"x", "q"})
    matching_doc_ids = index.exact_query({"x"})
    assert matching_doc_ids == {0, 2}

    # Also check that the set returned by the method is a separate object from what's stored in the index.
    # So mutating matching_doc_ids should not change what's inside the index
    matching_doc_ids.add(4)
    matching_doc_ids_returned_again = index.exact_query({"x"})
    assert matching_doc_ids_returned_again == {0, 2}


def test_exact_query_when_no_results_found() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    index.add(0, {"x"})
    index.add(1, {"y", "z"})
    index.add(2, {"x", "q"})
    matching_doc_ids = index.exact_query({"a"})
    assert matching_doc_ids == set()


def test_exact_query_with_multiple_targets() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    index.add(0, {"x"})
    index.add(1, {"y", "z"})
    index.add(2, {"x", "q"})
    matching_doc_ids = index.exact_query({"y", "q"})
    assert matching_doc_ids == {1, 2}


def test_exact_query_with_zero_targets() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    index.add(0, {"x"})
    matching_doc_ids = index.exact_query(set())
    assert matching_doc_ids == set()


def test_exact_query_with_nonexact_fuzzy_matches_doesnt_return_fuzzy_matches() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    index.add(0, {"apple"})
    matching_doc_ids = index.exact_query({"air"})  # A fuzzy match, but not an exact match
    assert matching_doc_ids == set()


def test_fuzzy_query_when_returning_everything() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    index.add(0, {"foo"})
    index.add(1, {"fad"})
    matching_doc_ids = index.fuzzy_query("fxy", max_candidates=10)
    assert matching_doc_ids == {0, 1}


def test_fuzzy_query_with_some_results_removed_by_similarity_test() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=ExactComparisonKeywordSimilarityTest()
    )
    index.add(0, {"foo"})
    index.add(1, {"fad"})
    matching_doc_ids = index.fuzzy_query("fxy", max_candidates=10)
    assert matching_doc_ids == set()


def test_fuzzy_query_with_some_results_removed_by_similarity_test_v2() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    index.add(0, {"foo"})
    index.add(1, {"gab"})
    matching_doc_ids = index.fuzzy_query("fxy", max_candidates=10)
    assert matching_doc_ids == {0}


def test_fuzzy_query_with_some_results_removed_by_max_candidates_limit() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=AlwaysTrueComparisonKeywordSimilarityTest()
    )
    index.add(0, {"foo"})  # embedding vector is closer to target
    index.add(1, {"bar"})  # embedding vector is further from target
    matching_doc_ids = index.fuzzy_query("xyz", max_candidates=1)  # only one candidate possible
    assert matching_doc_ids == {0}


def test_fuzzy_query_with_keyword_appearing_in_multiple_docs() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=AlwaysTrueComparisonKeywordSimilarityTest()
    )
    index.add(0, {"foo"})
    index.add(1, {"foo"})
    index.add(2, {"bar"})
    matching_doc_ids = index.fuzzy_query("xyz", max_candidates=1)  # only one candidate possible
    assert matching_doc_ids == {0, 1}


def test_fuzzy_query_with_doc_containing_multiple_keywords() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=AlwaysTrueComparisonKeywordSimilarityTest()
    )
    index.add(0, {"foo", "xyz"})
    index.add(1, {"bar", "abc"})
    matching_doc_ids = index.fuzzy_query("foo", max_candidates=1)  # only one candidate possible
    assert matching_doc_ids == {0}


def test_fuzzy_query_with_max_candidates_zero_is_rejected() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    with pytest.raises(ValueError):
        index.fuzzy_query("fxy", max_candidates=0)


def test_fuzzy_query_with_max_candidates_too_high_is_rejected() -> None:
    index = FuzzyIndex(
        embedder=DummyEmbedder(),
        vector_collection=ChromaVectorCollection(),
        keyword_similarity_test=FirstLetterComparisonKeywordSimilarityTest()
    )
    with pytest.raises(ValueError):
        index.fuzzy_query("fxy", max_candidates=1000000)


def test_independence_of_columns_in_fuzzy_index_collection() -> None:
    index_collection = FuzzyIndexCollection(
        field_names={"F1", "F2"},
        embedder=DummyEmbedder(),
        vector_collection_factory=ChromaVectorCollectionFactory(),
        keyword_similarity_test=ExactComparisonKeywordSimilarityTest()
    )

    parsed_doc = ParsedDocument(
        fields=[
            ParsedField(field_name="F1", values={"a"}),
            ParsedField(field_name="F2", values={"b"})
        ]
    )
    index_collection.add(0, parsed_doc)

    # Checking that we really are using different indexes for the different fields.
    assert index_collection.fuzzy_query("F1", "a", max_candidates=10) == {0}
    assert index_collection.fuzzy_query("F1", "b", max_candidates=10) == set()
    assert index_collection.fuzzy_query("F2", "a", max_candidates=10) == set()
    assert index_collection.fuzzy_query("F2", "b", max_candidates=10) == {0}
