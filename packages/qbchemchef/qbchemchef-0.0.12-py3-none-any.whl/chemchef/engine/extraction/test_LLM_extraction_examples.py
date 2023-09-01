from typing import Optional

import pytest

from chemchef.engine.extraction.extraction import OpenAIDocumentParser, DocumentExtractionResponseParsingError
from chemchef.engine.extraction.schemas import DocumentSchema, FieldSchema, ParsedDocument


def run_example(document: str, doc_schema: DocumentSchema,
                must_have_at_least_one: Optional[dict[str, set[str]]] = None,
                must_have_precisely: Optional[dict[str, set[str]]] = None,
                must_have_all: Optional[dict[str, set[str]]] = None,
                must_be_nonempty: Optional[set[str]] = None,
                must_be_empty: Optional[set[str]] = None) -> None:
    """
    :param must_have_precisely: Format: {field: target_values}. The extracted values must be precisely equal to the target values
    :param must_have_at_least_one: Format: {field: target_values}. The extracted values must include at least one of the target values
    :param must_have_all: Format {field: target_values}. The extracted values must include all of the target values
    :param must_be_nonempty: Format {fields}. The field must have at least one extracted value
    :param must_be_empty: Format {fields}. The field must have no extracted values
    """
    print(f'Document:\n  {document}')
    print(
        'Schema fields:\n' +
        '\n'.join(
            f"- {field.field_name}: optional={field.optional}, multi-valued={field.multivalued}, allowed values={field.allowed_values}, example values={field.example_values}"
            for field in doc_schema.fields
        )
    )

    parser = OpenAIDocumentParser()
    parsed_doc = parser.parse(document, doc_schema)
    print(
        'Parsed document:\n' +
        '\n'.join(
            f"- {field.field_name}: {', '.join(field.values) if field.values else '[None]'}"
            for field in parsed_doc.fields
        )
    )

    if must_have_precisely:
        for field, target_values in must_have_precisely.items():
            assert set(parsed_doc[field]) == set(target_values)

    if must_have_at_least_one:
        for field, target_values in must_have_at_least_one.items():
            assert any(value in parsed_doc[field] for value in target_values)

    if must_have_all:
        for field, target_values in must_have_all.items():
            assert all(value in parsed_doc[field] for value in target_values)

    if must_be_nonempty:
        for field in must_be_nonempty:
            assert len(parsed_doc[field]) > 0

    if must_be_empty:
        for field in must_be_empty:
            assert len(parsed_doc[field]) == 0


POLITICIANS_SCHEMA = DocumentSchema(
    fields=[
        FieldSchema(
            field_name="Politician name",
            optional=False,
            multivalued=False,
            example_values={"George Bush", "Donald Trump"}
        ),
        FieldSchema(
            field_name="Party",
            optional=True,
            multivalued=False,
            allowed_values={"Conservative", "Liberal", "Labour"}
        ),
        FieldSchema(
            field_name="Legacy",
            optional=True,
            multivalued=True,
            example_values={"Vietnam war", "Furlough scheme during pandemic", "Privatising the health service",
                            "Closing coal mines", "Exiting the European Union"}
        ),
        FieldSchema(
            field_name="Year of birth",
            optional=True,
            multivalued=False,
            example_values={"1966", "2003"}
        )
    ]
)


@pytest.mark.flaky(reruns=3)
def test_simple_case() -> None:
    run_example(
        document="Tony Blair is a former Labour prime minister of the UK. In 1997, he introduced a minimum wage. In 2003, he ordered the invasion of Iraq by British troops.",
        doc_schema=POLITICIANS_SCHEMA,
        must_have_precisely={"Politician name": {"Tony Blair"}, "Party": {"Labour"}},
        must_be_nonempty={"Legacy"},
        must_be_empty={"Year of birth"}
    )


@pytest.mark.flaky(reruns=3)
def test_with_factually_incorrect_document() -> None:
    run_example(
        document="Tony Blair is a former Conservative prime minister of the UK, known for his policies of austerity.",
        doc_schema=POLITICIANS_SCHEMA,
        must_have_precisely={"Politician name": {"Tony Blair"}, "Party": {"Conservative"}},
        must_be_nonempty={"Legacy"},
        must_be_empty={"Year of birth"}
    )


@pytest.mark.flaky(reruns=3)
def test_with_missing_mandatory_field() -> None:
    # Politician name is marked as mandatory, but this is only a soft instruction.
    # On this occasion, the computer ignores this instruction.
    run_example(
        document="He is a former Liberal prime minister of the UK who brought about the welfare state.",
        doc_schema=POLITICIANS_SCHEMA,
        must_have_precisely={"Party": {"Liberal"}},
        must_be_nonempty={"Legacy"},
        must_be_empty={"Politician name", "Year of birth"}
    )


@pytest.mark.flaky(reruns=3)
def test_with_two_values_for_single_valued_field_returns_most_clearcut_value() -> None:
    # The computer obeys the soft instruction to return only one political party (Conservative).
    run_example(
        document="David Lloyd George was originally a Liberal, but switched allegiances to the Conservative party.",
        doc_schema=POLITICIANS_SCHEMA,
        must_have_precisely={"Politician name": {"David Lloyd George"}},
        must_have_at_least_one={"Party": {"Conservative"}},
        must_be_empty={"Year of birth"}
    )


@pytest.mark.flaky(reruns=3)
def test_with_two_values_for_single_valued_field_with_equal_weight_returns_both() -> None:
    # The computer ignores the soft instruction and returns both political parties
    run_example(
        document="David Lloyd George was a member of the Liberal party during 1904-1924, and was a member of the Conservative party during 1924-1964.",
        doc_schema=POLITICIANS_SCHEMA,
        must_have_precisely={"Politician name": {"David Lloyd George"}, "Party": {"Liberal", "Conservative"}},
        must_be_empty={"Year of birth"}
    )


@pytest.mark.flaky(reruns=3)
def test_with_value_written_differently_from_allowed_value() -> None:
    # The party is written as "Tory", but the computer outputs "Conservative" as per the schema
    run_example(
        document="David Cameron was a Tory who cared only for the rich.",
        doc_schema=POLITICIANS_SCHEMA,
        must_have_precisely={"Politician name": {"David Cameron"}, "Party": {"Conservative"}},
        must_be_empty={"Year of birth"}
    )


@pytest.mark.flaky(reruns=3)
def test_with_value_different_from_all_allowed_values() -> None:
    # The party is not accurately represented by "Conservative", "Liberal" or "Labour".
    run_example(
        document="Caroline Lucas was the first and only Green Party member to be elected as MP. Born in 1960, she served as MP for Brighton Pavilion from 2010.",
        doc_schema=POLITICIANS_SCHEMA,
        must_have_precisely={"Politician name": {"Caroline Lucas"}, "Year of birth": {"1960"}},
        must_have_at_least_one={"Party": {"Green", "Green Party"}}
    )


@pytest.mark.flaky(reruns=3)
def test_with_wrong_subject() -> None:
    # The document is not about a politician at all, so the computer extracts nothing.
    run_example(
        document="Zinedine Zidane was the captain of the French national football team.",
        doc_schema=POLITICIANS_SCHEMA,
        must_be_empty={"Politician name", "Party", "Legacy", "Year of birth"}
    )
