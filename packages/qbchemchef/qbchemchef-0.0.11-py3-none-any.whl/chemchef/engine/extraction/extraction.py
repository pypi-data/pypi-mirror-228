import logging
from abc import ABC, abstractmethod

from pydantic import BaseModel

from chemchef.clients.openai import OpenAIChatHandler, ChatMessage, SystemMessage, UserMessage, AssistantMessage
from chemchef.engine.extraction.schemas import FieldSchema, DocumentSchema, ParsedField, ParsedDocument


class AbstractDocumentParser(ABC):
    """A method for extracting structured information from unstructured documents."""

    @abstractmethod
    def parse(self, document: str, doc_schema: DocumentSchema) -> ParsedDocument:
        """
        :param document: The unstructured document
        :param doc_schema: The schema, defining the format of the structured info that should be extracted from the document
        :return: the structured info extracted from the document
        """
        raise NotImplementedError


def construct_field_description(field_schema: FieldSchema) -> str:
    if field_schema.optional:
        if field_schema.multivalued:
            multiplicity_description = "Sometimes populated, may be multi-valued when populated."
        else:
            multiplicity_description = "Sometimes populated, usually single-valued when populated."
    else:
        if field_schema.multivalued:
            multiplicity_description = "Usually populated, may be multi-valued."
        else:
            multiplicity_description = "Usually populated, usually single-valued."

    if field_schema.allowed_values is not None:
        allowed_or_example_values_description = "Example values (use these where possible): {}.".format(', '.join(field_schema.allowed_values))
    elif field_schema.example_values is not None:
        allowed_or_example_values_description = "Example values: {}.".format(', '.join(field_schema.example_values))
    else:
        allowed_or_example_values_description = ""

    return f"{field_schema.field_name}: {multiplicity_description} {allowed_or_example_values_description}"


def construct_document_schema_description(doc_schema: DocumentSchema) -> str:
    return '\n'.join(construct_field_description(field) for field in doc_schema.fields)


USER_MESSAGE = "Extract the following fields from the text.\n\n***Fields to extract***\n{}\n\n***Text***\n{}"


def construct_user_message(document: str, doc_schema: DocumentSchema) -> str:
    return USER_MESSAGE.format(
        construct_document_schema_description(doc_schema),
        document
    )


def construct_assistant_message(parsed_doc: ParsedDocument) -> str:
    return "\n".join(
        "{}: {}".format(field.field_name, ', '.join(field.values))
        for field in parsed_doc.fields
    )


class DocumentExtractionResponseParsingError(Exception):
    pass


def parse_assistant_message_line(message_line: str, field_schema: FieldSchema) -> ParsedField:
    expected_line_header = f"{field_schema.field_name}:"
    if not message_line.startswith(expected_line_header):
        raise DocumentExtractionResponseParsingError(
            f"Cannot parse chat response - line header does not match field name {field_schema.field_name}: {message_line}"
        )
    message_line_without_header = message_line[len(expected_line_header):].strip()

    values = {
        value.strip() for value in message_line_without_header.split(', ')
        if len(value.strip()) > 0
    }

    return ParsedField(field_name=field_schema.field_name, values=values)


def parse_assistant_message(message_contents: str, doc_schema: DocumentSchema) -> ParsedDocument:
    message_lines = message_contents.strip().splitlines()
    if not len(message_lines) == len(doc_schema.fields):
        raise DocumentExtractionResponseParsingError(
            f"Cannot parse chat response - wrong number of lines: {message_contents}"
        )

    parsed_fields = [parse_assistant_message_line(line, field_schema)
                     for line, field_schema in zip(message_lines, doc_schema.fields)]
    return ParsedDocument(fields=parsed_fields)


class ExtractionTaskExample(BaseModel):
    document: str
    doc_schema: DocumentSchema
    parsed_doc: ParsedDocument


SYSTEM_MESSAGE = "The AI assistant extracts information from documents. "\
                 "The assistant must only use information contained in the doument. "\
                 "The assistant's response must reflect the intent of the document "\
                 "(even if the document is factually incorrect)."


EXAMPLES: list[ExtractionTaskExample] = [
    ExtractionTaskExample(
        document="Chocolate brownie recipe: Mix melted chocolate with sugar and flour in a bowl, "
                 "and bake for 20 minutes.",
        doc_schema=DocumentSchema(
            fields=[
                FieldSchema(
                    field_name="Dish",
                    optional=False,
                    multivalued=False,
                    example_values={"Chicken curry", "Sponge cake"}
                ),
                FieldSchema(
                    field_name="Ingredients",
                    optional=False,
                    multivalued=True,
                    example_values={"Chicken", "Fish", "Eggs", "Butter", "Apples"}
                ),
                FieldSchema(
                    field_name="Cuisine",
                    optional=True,
                    multivalued=False,
                    allowed_values={"Chinese", "Indian"}
                )
            ]
        ),
        parsed_doc=ParsedDocument(
            fields=[
                ParsedField(
                    field_name="Dish",
                    values={"Chocolate brownie"}
                ),
                ParsedField(
                    field_name="Ingredients",
                    values={"Chocolate", "Sugar", "Flour"}
                ),
                ParsedField(
                    field_name="Cuisine",
                    values=set()  # missing from document
                )
            ]
        )
    ),
    ExtractionTaskExample(
        document="Property to let: Stylish modern one-bed apartment with stunning views of downtown Boston.",
        doc_schema=DocumentSchema(
            fields=[
                FieldSchema(
                    field_name="Advert type",
                    optional=False,
                    multivalued=False,
                    allowed_values={"Letting", "Sale"}
                ),
                FieldSchema(
                    field_name="City",
                    optional=False,
                    multivalued=False,
                    example_values={"London", "New York"}
                ),
                FieldSchema(
                    field_name="Number of bedrooms",
                    optional=True,
                    multivalued=False,
                    allowed_values={"Studio", "One bedroom", "Two bedrooms"}
                ),
                FieldSchema(
                    field_name="Furnished",
                    optional=True,
                    multivalued=False,
                    allowed_values={"Yes", "No"}
                )
            ]
        ),
        parsed_doc=ParsedDocument(
            fields=[
                ParsedField(
                    field_name="Advert type",
                    values={"Letting"}
                ),
                ParsedField(
                    field_name="City",
                    values={"Boston"}
                ),
                ParsedField(
                    field_name="Number of bedrooms",
                    values={"One bedroom"}  # formatted as "one-bed" in the document, but "One bedroom" is an allowed value
                ),
                ParsedField(
                    field_name="Furnished",
                    values=set()  # missing from document
                )
            ]
        )
    ),
    ExtractionTaskExample(
        document="Mohammed Salah plays as striker for Liverpool FC.",
        doc_schema=DocumentSchema(
            fields=[
                FieldSchema(
                    field_name="Player",
                    optional=False,
                    multivalued=False,
                    example_values={"Cristiano Ronaldo", "Lionel Messi"}
                ),
                FieldSchema(
                    field_name="Club team",
                    optional=True,
                    multivalued=False,
                    example_values={"Manchester United", "Arsenal"}
                ),
                FieldSchema(
                    field_name="National team",
                    optional=True,
                    multivalued=False,
                    example_values={"England", "France"}
                ),
                FieldSchema(
                    field_name="Position",
                    optional=True,
                    multivalued=False,
                    allowed_values={"Forward", "Midfielder", "Defender", "Goalkeeper"}
                )
            ]
        ),
        parsed_doc=ParsedDocument(
            fields=[
                ParsedField(
                    field_name="Player",
                    values={"Mohammed Salah"}
                ),
                ParsedField(
                    field_name="Club team",
                    values={"Liverpool FC"}
                ),
                ParsedField(
                    field_name="National team",
                    values=set()  # missing from document
                ),
                ParsedField(
                    field_name="Position",
                    values={"Forward"}  # described as "striker" in the document, but "Forward" is an allowed value
                )
            ]
        )
    ),
    ExtractionTaskExample(
        document="Mohammed Salah is Everton's number 1 goalkeeper.",
        doc_schema=DocumentSchema(
            fields=[
                FieldSchema(
                    field_name="Player",
                    optional=False,
                    multivalued=False,
                    example_values={"Cristiano Ronaldo", "Lionel Messi"}
                ),
                FieldSchema(
                    field_name="Club team",
                    optional=True,
                    multivalued=False,
                    example_values={"Manchester United", "Arsenal"}
                ),
                FieldSchema(
                    field_name="Position",
                    optional=True,
                    multivalued=False,
                    allowed_values={"Forward", "Midfielder", "Defender", "Goalkeeper"}
                )
            ]
        ),
        parsed_doc=ParsedDocument(
            fields=[
                ParsedField(
                    field_name="Player",
                    values={"Mohammed Salah"}
                ),
                ParsedField(
                    field_name="Club team",
                    values={"Everton"}  # factually false, but faithful to the document
                ),
                ParsedField(
                    field_name="Position",
                    values={"Goalkeeper"}  # factually false, but faithful to the document
                )
            ]
        )
    ),
    ExtractionTaskExample(
        document="Mohammed Salah is a very good football player.",
        doc_schema=DocumentSchema(
            fields=[
                FieldSchema(
                    field_name="Player",
                    optional=False,
                    multivalued=False,
                    example_values={"Cristiano Ronaldo", "Lionel Messi"}
                ),
                FieldSchema(
                    field_name="Club team",
                    optional=True,
                    multivalued=False,
                    example_values={"Manchester United", "Arsenal"}
                ),
                FieldSchema(
                    field_name="Position",
                    optional=True,
                    multivalued=False,
                    allowed_values={"Forward", "Midfielder", "Defender", "Goalkeeper"}
                )
            ]
        ),
        parsed_doc=ParsedDocument(
            fields=[
                ParsedField(
                    field_name="Player",
                    values={"Mohammed Salah"}
                ),
                ParsedField(
                    field_name="Club team",
                    values=set()  # This info is surely in ChatGPT's training data, but it's not in the document
                ),
                ParsedField(
                    field_name="Position",
                    values=set()  # This info is surely in ChatGPT's training data, but it's not in the document
                )
            ]
        )
    ),
    ExtractionTaskExample(
        # This document is not about a football player, so the data fields can't be extracted.
        document="Chairman Mao Tze Tung was the leader of the Chinese Communist Party between 1943 and 1976.",
        doc_schema=DocumentSchema(
            fields=[
                FieldSchema(
                    field_name="Player",
                    optional=False,
                    multivalued=False,
                    example_values={"Cristiano Ronaldo", "Lionel Messi"}
                ),
                FieldSchema(
                    field_name="Club team",
                    optional=False,
                    multivalued=False,
                    example_values={"Manchester United", "Arsenal"}
                ),
                FieldSchema(
                    field_name="Position",
                    optional=False,
                    multivalued=False,
                    allowed_values={"Forward", "Midfielder", "Defender", "Goalkeeper"}
                )
            ]
        ),
        parsed_doc=ParsedDocument(
            fields=[
                ParsedField(
                    field_name="Player",
                    values=set()  # empty, even though the field is "usually required"
                ),
                ParsedField(
                    field_name="Club team",
                    values=set()  # empty, even though the field is "usually required"
                ),
                ParsedField(
                    field_name="Position",
                    values=set()  # empty, even though the field is "usually required"
                )
            ]
        )
    )
]


class OpenAIDocumentParser(AbstractDocumentParser):

    def __init__(self) -> None:
        self._chat_handler = OpenAIChatHandler()

    def parse(self, doc: str, doc_schema: DocumentSchema) -> ParsedDocument:
        prompts = self._construct_prompt(doc, doc_schema)
        response = self._chat_handler.run(prompts)
        return self._parse_response(response, doc_schema)

    @staticmethod
    def _construct_prompt(document: str, doc_schema: DocumentSchema) -> list[ChatMessage]:
        messages: list[ChatMessage] = []

        messages.append(SystemMessage(content=SYSTEM_MESSAGE))

        for example in EXAMPLES:
            messages.append(UserMessage(
                content=construct_user_message(example.document, example.doc_schema)))
            messages.append(AssistantMessage(
                content=construct_assistant_message(example.parsed_doc)))

        messages.append(UserMessage(
            content=construct_user_message(document, doc_schema)))

        return messages

    @staticmethod
    def _parse_response(response: AssistantMessage, doc_schema: DocumentSchema) -> ParsedDocument:
        logging.debug("Response from ChatGPT for similarity test: %s", response.content)
        parsed_doc = parse_assistant_message(response.content, doc_schema)
        return parsed_doc
