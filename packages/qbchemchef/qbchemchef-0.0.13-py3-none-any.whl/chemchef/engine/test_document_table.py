from typing import Any, Iterable, Optional
import numpy as np
import pytest

from chemchef.clients.chroma.chroma_client import ChromaVectorCollectionFactory
from chemchef.clients.openai import AbstractEmbedder
from chemchef.engine.document_table import DocumentTable
from chemchef.engine.extraction import DocumentSchema, FieldSchema, AbstractDocumentParser, ParsedDocument, ParsedField
from chemchef.engine.generation import AbstractDocumentGenerator
from chemchef.engine.indexing import AbstractKeywordSimilarityTest, Exact, Fuzzy

FORMAT_DESCRIPTION = "Animal factsheet"

MAIN_DOC_SCHEMA = DocumentSchema(
    fields=[
        FieldSchema(field_name="Animal", optional=False, multivalued=False),
        FieldSchema(field_name="Sound", optional=False, multivalued=False)
    ]
)

SUBJECT_FIELD = "Animal"


class DummyDocumentParser(AbstractDocumentParser):
    """
    e.g.
      document='cat meow'
      doc_schema=[Animal, Sound]
    =>
      parsed_doc=[Animal=cat, Sound=meow]
    """

    def parse(self, document: str, doc_schema: DocumentSchema) -> ParsedDocument:
        words = document.split()
        assert len(words) == len(doc_schema.fields)
        return ParsedDocument(
            fields=[
                ParsedField(field_name=field.field_name, values={word})
                for word, field in zip(words, doc_schema.fields)
            ]
        )


class DummyDocumentGenerator(AbstractDocumentGenerator):
    """
    e.g.
       subject=cat
       expected_contents=[Sound]
    =>
       generated_doc='cat boo_sound'

       ... unless subject is 'Tiger', in which case the None pointer will be generated
    """

    def generate(self, subject: str, format: str, expected_contents: Iterable[str]) -> Optional[str]:
        if subject == 'Tiger':
            return None
        elif subject == 'Lion':
            words = ['Gorilla'] + ['boo_' + field for field in expected_contents]
            return ' '.join(words)
        else:
            words = [subject] + ['boo_' + field for field in expected_contents]
            return ' '.join(words)


class DummyEmbedder(AbstractEmbedder):
    """Every keyword is assigned the zero embedding vector"""

    def embed(self, text: str) -> np.ndarray[np.float64, Any]:
        return np.array([0.0])


class DummyKeywordSimilarityTest(AbstractKeywordSimilarityTest):
    """First letters matches => deemed a match"""

    def find_matches(self, target_keyword: str, candidate_keywords: Iterable[str]) -> set[str]:
        return {
            keyword for keyword in candidate_keywords
            if len(keyword) > 0 and len(target_keyword) > 0 and keyword[0] == target_keyword[0]
        }


def create_table(document_schema: DocumentSchema = MAIN_DOC_SCHEMA, subject_field:  str = SUBJECT_FIELD) -> DocumentTable:
    return DocumentTable(
         format_description=FORMAT_DESCRIPTION,
         document_schema=document_schema,
         subject_field=subject_field,
         document_parser=DummyDocumentParser(),
         document_auto_generator=DummyDocumentGenerator(),
         embedder=DummyEmbedder(),
         vector_collection_factory=ChromaVectorCollectionFactory(),
         keyword_similarity_test=DummyKeywordSimilarityTest()
    )


def test_constructor_rejects_schema_without_fields() -> None:
    doc_schema = DocumentSchema(fields=[])
    with pytest.raises(ValueError) as exc_info:
        create_table(doc_schema)

    assert "at least one" in str(exc_info.value)


def test_constructor_rejects_schema_with_duplicate_field_names() -> None:
    doc_schema = DocumentSchema(fields=[
        FieldSchema(field_name="Animal", optional=False, multivalued=False),
        FieldSchema(field_name="Animal", optional=False, multivalued=True)
    ])
    with pytest.raises(ValueError) as exc_info:
        create_table(doc_schema)

    assert "distinct" in str(exc_info.value)


def test_constructor_rejects_schema_whose_fields_do_not_include_subject_name() -> None:
    with pytest.raises(ValueError) as exc_info:
        create_table(subject_field="Non-existent")

    assert "subject field" in str(exc_info.value)


def test_insert_returns_stored_doc() -> None:
    table = create_table()
    stored_doc = table.insert("Cat meow")

    assert stored_doc.id == 0
    assert stored_doc.text == "Cat meow"
    assert stored_doc.parsed_data.to_dict() == {'Animal': {'Cat'}, 'Sound': {'meow'}}


def test_insert_with_subject_explicitly_passed_in() -> None:
    table = create_table()
    stored_doc = table.insert("Cat meow", subject="Chimp")  # overriding the subject

    assert stored_doc.id == 0
    assert stored_doc.text == "Cat meow"
    assert stored_doc.parsed_data.to_dict() == {'Animal': {'Chimp'}, 'Sound': {'meow'}}


def test_query_after_insert() -> None:
    table = create_table()
    table.insert("Cat meow")
    table.insert("Dog woof")

    query_results = table.query(Exact(field="Animal", targets={"Cat"}) & Exact(field="Sound", targets={"meow"}))

    assert len(query_results) == 1
    assert query_results[0].id == 0
    assert query_results[0].text == "Cat meow"
    assert query_results[0].parsed_data.to_dict() == {'Animal': {'Cat'}, 'Sound': {'meow'}}

    query_results_2 = table.query(Fuzzy(field="Animal", target="Ddd"))  # Ddd will fuzzy-match Dog

    assert len(query_results_2) == 1
    assert query_results_2[0].id == 1
    assert query_results_2[0].text == "Dog woof"
    assert query_results_2[0].parsed_data.to_dict() == {'Animal': {'Dog'}, 'Sound': {'woof'}}


def test_query_after_auto_insert() -> None:
    table = create_table()
    generated_doc = table.auto_insert("Cat")

    assert generated_doc is not None
    assert generated_doc.id == 0
    assert generated_doc.text == "Cat boo_Sound"
    assert generated_doc.parsed_data.to_dict() == {'Animal': {'Cat'}, 'Sound': {'boo_Sound'}}

    query_results = table.query(Exact(field="Animal", targets={"Cat"}))

    assert len(query_results) == 1
    assert query_results[0].id == 0
    assert query_results[0].text == "Cat boo_Sound"
    assert query_results[0].parsed_data.to_dict() == {'Animal': {'Cat'}, 'Sound': {'boo_Sound'}}


def test_query_after_auto_insert_with_subject_deemed_incompatible() -> None:
    table = create_table()
    generated_doc = table.auto_insert('Tiger')

    assert generated_doc is None

    query_results = table.query(Exact(field="Animal", targets={"Tiger"}))
    assert len(query_results) == 0


def test_query_after_auto_insert_when_auto_generated_doc_has_wrong_subject() -> None:
    table = create_table()
    generated_doc = table.auto_insert('Lion')

    # Our implementation will generate text about a gorilla, but our code should fix this.

    assert generated_doc is not None

    query_results = table.query(Exact(field="Animal", targets={"Lion"}))
    assert len(query_results) == 1
    assert query_results[0].parsed_data['Animal'] == {'Lion'}


def test_query_after_auto_insert_with_existing_document_on_subject() -> None:
    table = create_table()
    inserted_doc = table.insert('Cat meow')
    possibly_generated_doc = table.auto_insert('Cat')  # ...but there already is a document on cats!

    assert possibly_generated_doc is not None
    assert inserted_doc.id == possibly_generated_doc.id
    assert inserted_doc.text == possibly_generated_doc.text


def test_query_with_no_query_expr_returns_all_docs() -> None:
    table = create_table()
    table.insert("Cat meow")
    table.insert("Dog woof")

    query_results = table.query()

    assert len(query_results) == 2
