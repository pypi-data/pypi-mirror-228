from chemchef.engine.generation.generation import construct_user_message, parse_assistant_message, INCOMPATIBILITY_TOKEN


def test_construct_user_message() -> None:
    message = construct_user_message("Apples", "Dietary factsheet", ["Calories per 100g", "Vegetarian/Non-vegetarian"])
    assert "Subject: Apples" in message
    assert "Format: Dietary factsheet" in message
    assert "Contents to include: calories per 100g, vegetarian/non-vegetarian" in message


def test_parse_assistant_message() -> None:
    message = "\n\n This is so awesome!!!   \nThat's my opinion anyway.\n\n\n"
    subject = "Thoughts"

    parsed_message = parse_assistant_message(message, subject)

    assert parsed_message == "Topic: Thoughts\nThis is so awesome!!!\nThat's my opinion anyway."


def test_parse_assistant_message_when_subject_deemed_incompatible() -> None:
    message = INCOMPATIBILITY_TOKEN
    subject = "Stuff"

    parsed_message = parse_assistant_message(message, subject)

    assert parsed_message is None
