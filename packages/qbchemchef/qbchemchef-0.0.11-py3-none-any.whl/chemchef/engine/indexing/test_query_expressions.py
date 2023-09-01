import pytest

from chemchef.clients.chroma.chroma_client import ChromaVectorCollectionFactory
from chemchef.engine.extraction import ParsedDocument, ParsedField
from chemchef.engine.indexing import FuzzyIndexCollection, Exact, Fuzzy, All
from chemchef.engine.indexing.test_fuzzy_index import DummyEmbedder, FirstLetterComparisonKeywordSimilarityTest


def create_fuzzy_index_collection() -> FuzzyIndexCollection:
    indexes = FuzzyIndexCollection(
        {"Name", "Properties"},
        DummyEmbedder(),
        ChromaVectorCollectionFactory(),
        FirstLetterComparisonKeywordSimilarityTest()
    )

    indexes.add(
        document_id=0,
        parsed_doc=ParsedDocument(
            fields=[
                ParsedField(field_name="Name", values={"Alice"}),
                ParsedField(field_name="Properties", values={"American", "Elderly"}),
            ]
        )
    )

    indexes.add(
        document_id=1,
        parsed_doc=ParsedDocument(
            fields=[
                ParsedField(field_name="Name", values={"Bob"}),
                ParsedField(field_name="Properties", values={"British"})
            ]
        )
    )

    return indexes


def test_exact_query() -> None:
    indexes = create_fuzzy_index_collection()
    expr = Exact(field="Name", targets={"Alice"})
    results = expr.to_query().run(indexes)
    assert results == {0}


def test_exact_query_with_nonexistent_field() -> None:
    indexes = create_fuzzy_index_collection()
    expr = Exact(field="Non-existent", targets={"foo"})
    with pytest.raises(KeyError):
        expr.to_query().run(indexes)


def test_fuzzy_query() -> None:
    indexes = create_fuzzy_index_collection()
    expr = Fuzzy(field="Name", target="BBB")  # matches "Bob", since criterion is first letter match
    results = expr.to_query().run(indexes)
    assert results == {1}


def test_fuzzy_query_with_nonexistent_field() -> None:
    indexes = create_fuzzy_index_collection()
    expr = Fuzzy(field="Non-existent", target="foo")
    with pytest.raises(KeyError):
        expr.to_query().run(indexes)


def test_and_query() -> None:
    indexes = create_fuzzy_index_collection()
    expr = Fuzzy(field="Name", target="BBB") & Exact(field="Properties", targets={"British"})
    results = expr.to_query().run(indexes)
    assert results == {1}


def test_and_query_v2() -> None:
    indexes = create_fuzzy_index_collection()
    expr = Fuzzy(field="Name", target="BBB") & Exact(field="Properties", targets={"American"})
    results = expr.to_query().run(indexes)
    assert results == set()


def test_or_query() -> None:
    indexes = create_fuzzy_index_collection()
    expr = Fuzzy(field="Name", target="BBB") | Exact(field="Properties", targets={"British"})
    results = expr.to_query().run(indexes)
    assert results == {1}


def test_or_query_v2() -> None:
    indexes = create_fuzzy_index_collection()
    expr = Fuzzy(field="Name", target="BBB") | Exact(field="Properties", targets={"American"})
    results = expr.to_query().run(indexes)
    assert results == {0, 1}


def test_not_query() -> None:
    indexes = create_fuzzy_index_collection()
    expr = ~Exact(field="Name", targets={"Alice"})
    results = expr.to_query().run(indexes)
    assert results == {1}


def test_all_query() -> None:
    indexes = create_fuzzy_index_collection()
    expr = All()
    results = expr.to_query().run(indexes)
    assert results == {0, 1}
