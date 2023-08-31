from chemchef.clients.chroma.chroma_client import ChromaVectorCollection
import numpy as np


def test_query_without_add_returns_nothing() -> None:
    collection = ChromaVectorCollection()
    results = collection.query(np.array([1.0, 2.0]), max_results=5)
    assert len(results) == 0


def test_query_with_some_adds_returns_most_relevant_documents() -> None:
    collection = ChromaVectorCollection()
    collection.add(np.array([1.5, 0.0]), "bar")
    collection.add(np.array([-1.0, 0.0]), "aaa")
    collection.add(np.array([2.0, 0.0]), "foo")
    collection.add(np.array([1.0, 0.0]), "xyz")
    collection.add(np.array([6.0, 99.0]), "bbb")
    results = collection.query(np.array([6.0, 0.0]), max_results=2)
    assert results == ["foo", "bar"]


def test_query_with_with_max_num_results_exceeding_total_documents_returns_documents_in_descending_order_of_relevance() -> None:
    collection = ChromaVectorCollection()
    collection.add(np.array([1.5, 0.0]), "bar")
    collection.add(np.array([-1.0, 0.0]), "aaa")
    collection.add(np.array([2.0, 0.0]), "foo")
    collection.add(np.array([1.0, 0.0]), "xyz")
    collection.add(np.array([6.0, 99.0]), "bbb")
    results = collection.query(np.array([6.0, 0.0]), max_results=7)
    assert results == ["foo", "bar", "xyz", "aaa", "bbb"]


def test_adds_with_other_collections_created_only_modifies_this_collection() -> None:
    collection1 = ChromaVectorCollection()
    collection2 = ChromaVectorCollection()
    collection1.add(np.array([0.9]), "foo")
    collection2.add(np.array([1.1]), "bar")
    results = collection1.query(np.array([1.0]), max_results=6)
    assert results == ["foo"]

