import pytest

from chemchef.engine.extraction.extraction import construct_user_message, construct_assistant_message, \
    parse_assistant_message, DocumentExtractionResponseParsingError
from chemchef.engine.extraction.schemas import DocumentSchema, FieldSchema, ParsedField, ParsedDocument

DOC_SCHEMA = DocumentSchema(
        fields=[
            FieldSchema(
                field_name="Dish",
                optional=False,
                multivalued=False,
                example_values={"Chicken curry", "Beef stew"}
            ),
            FieldSchema(
                field_name="Ingredients",
                optional=False,
                multivalued=True,
                example_values={"Eggs", "Fish"}
            ),
            FieldSchema(
                field_name="Cuisine",
                optional=True,
                multivalued=False,
                allowed_values={"Chinese", "Indian"}
            )
        ]
    )


def test_construct_user_message() -> None:
    document = "Mix the butter and the sugar. Beat in the eggs. Sift in the flour. Bake for 40 minutes. This should produce the perfect sponge cake."
    message = construct_user_message(document, DOC_SCHEMA)
    assert ("Dish: Usually populated, usually single-valued. Example values: Chicken curry, Beef stew." in message or
            "Dish: Usually populated, usually single-valued. Example values: Beef stew, Chicken curry." in message)
    assert ("Ingredients: Usually populated, may be multi-valued. Example values: Eggs, Fish." in message or
            "Ingredients: Usually populated, may be multi-valued. Example values: Fish, Eggs." in message)
    assert ("Sometimes populated, usually single-valued when populated. Example values (use these where possible): Chinese, Indian" in message or
            "Sometimes populated, usually single-valued when populated. Example values (use these where possible): Indian, Chinese" in message)
    assert document in message


def test_construct_assistant_message() -> None:
    parsed_doc = ParsedDocument(
        fields=[
            ParsedField(field_name="Dish", values={"Sponge cake"}),
            ParsedField(field_name="Ingredients", values={"Butter", "Sugar"}),
            ParsedField(field_name="Cuisine", values=set())
        ]
    )
    message = construct_assistant_message(parsed_doc)
    message_lines = message.split('\n')
    assert message_lines[0] == "Dish: Sponge cake"
    assert message_lines[1] == "Ingredients: Butter, Sugar" or message_lines[1] == "Ingredients: Sugar, Butter"
    assert message_lines[2] == "Cuisine: "


def test_extract_assistant_message_with_valid_response() -> None:
    message = "Dish: Sponge cake\nIngredients: Butter, Sugar\nCuisine: "
    parsed_doc = parse_assistant_message(message, DOC_SCHEMA)
    assert parsed_doc == ParsedDocument(
        fields=[
            ParsedField(field_name="Dish", values={"Sponge cake"}),
            ParsedField(field_name="Ingredients", values={"Butter", "Sugar"}),
            ParsedField(field_name="Cuisine", values=set())
        ]
    )


def test_extract_assistant_message_with_wrong_number_of_lines() -> None:
    message = "Dish: Sponge cake\nIngredients: Butter, Sugar\nCuisine: \nExtra line"

    with pytest.raises(DocumentExtractionResponseParsingError) as exc_info:
        parse_assistant_message(message, DOC_SCHEMA)

    assert "wrong number of lines" in str(exc_info.value)


def test_extract_assistant_message_with_wrong_line_header() -> None:
    message = "Wrong header: Sponge cake\nIngredients: Butter, Sugar\nCuisine: "

    with pytest.raises(DocumentExtractionResponseParsingError) as exc_info:
        parse_assistant_message(message, DOC_SCHEMA)

    assert "line header does not match field name Dish" in str(exc_info.value)
