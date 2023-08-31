import logging
from abc import ABC, abstractmethod
from typing import Iterable, Optional

from pydantic import BaseModel

from chemchef.clients.openai import OpenAIChatHandler, ChatMessage, SystemMessage, UserMessage, AssistantMessage


class AbstractDocumentGenerator(ABC):
    """A method for generating a document on a particular subject."""

    @abstractmethod
    def generate(self, subject: str, format: str, expected_contents: Iterable[str]) -> Optional[str]:
        """
        :param subject: The subject of the document.
            e.g. "Victoria sponge cake"
        :param format: A description of the format of the document to generate.
            e.g. "Recipe"
        :param expected_contents: Some types of content that the generated document should include within its text.
            e.g. ["Ingredients", "Cooking time", "Cuisine"]
        :return: The generated document - a freeform, unstructured piece of text.
                 OR the None pointer, if the subject and format are incompatible
        """
        raise NotImplementedError


INCOMPATIBILITY_TOKEN = "INVALID"  # used as a response if the inputs are invalid

SYSTEM_MESSAGE = f"The AI assistant generates texts on a topic specified by the user. "\
                 "The documents generated should be neutral in tone. "\
                 "The documents should be based on either facts or standard practice, "\
                 "and should avoid bias wherever possible. "\
                 "The documents should be concise (i.e. no more than 200 words). "\
                 "If it is not possible to generate a document "\
                 "(e.g. because of a logical mismatch between the subject and the intended document format), "\
                 f"then the assistant responds with the word '{INCOMPATIBILITY_TOKEN}'."

USER_MESSAGE_TEMPLATE = "Subject: {}\nFormat: {}\nContents to include: {}"


class DocumentGenerationError(Exception):
    pass


def construct_user_message(subject: str, format: str, expected_contents: Iterable[str]) -> str:
    return USER_MESSAGE_TEMPLATE.format(
        subject,
        format,
        ', '.join(content_type.lower() for content_type in expected_contents)
    )


def construct_assistant_message(output: Optional[str]) -> str:
    if output is None:
        return INCOMPATIBILITY_TOKEN
    else:
        return output


def parse_assistant_message(message: str, subject: str) -> Optional[str]:
    if message.strip() == INCOMPATIBILITY_TOKEN:
        return None

    # Remove consecutive newline characters
    lines = [line.strip() for line in message.strip().splitlines() if len(line.strip()) > 0]
    message = '\n'.join(lines)

    # Append the subject as a header.
    return 'Topic: {}\n{}'.format(subject, message)


class DocumentGenerationTaskExample(BaseModel):
    subject: str
    format: str
    expected_contents: list[str]
    output: Optional[str]


EXAMPLES: list[DocumentGenerationTaskExample] = [
    DocumentGenerationTaskExample(
        subject="Chocolate sponge cake",
        format="Recipe",
        expected_contents=["Ingredients", "Cooking time"],
        output="Preheat oven to 350°F (175°C). Grease and flour an 8-inch cake tin. "
               "In a large bowl, sift together 1 cup of all-purpose flour, 1/2 cup of unsweetened cocoa powder, "
               "1 and 1/2 teaspoons of baking powder, and 1/4 teaspoon of salt. "
               "In another bowl, cream together 1/2 cup of unsalted butter and 1 cup of sugar until light and fluffy. "
               "Beat in 2 large eggs, one at a time, followed by 1 teaspoon of vanilla extract. "
               "Gradually mix in the dry ingredients, alternating with 1/2 cup of milk. "
               "Pour batter into the prepared tin and smooth the top. "
               "Bake for 25-30 minutes, or until a toothpick inserted into the center comes out clean. "
               "Cool in the tin for 10 minutes, then transfer to a wire rack to cool completely."
    ),
    DocumentGenerationTaskExample(
        subject="Donald Trump",
        format="Politician biography",
        expected_contents=["Date of birth", "Educational institutions", "Legacy"],
        output="Donald J. Trump was born on June 14, 1946, in Queens, New York. "
               "He graduated from the Wharton School of the University of Pennsylvania in 1968. "
               "Before entering politics, Trump built a career in real estate as the head of The Trump Organization, "
               "managing and developing properties, hotels, casinos, and golf courses worldwide. "
               "He also gained fame as a reality TV star on The Apprentice. "
               "Trump entered the political arena and, in 2016, secured the Republican nomination for president. "
               "Despite facing criticism and controversy during his campaign, he was elected the 45th president "
               "of the United States, serving from January 2017 to January 2021. "
               "His presidency was marked by a focus on deregulation, tax cuts, and a hardline immigration stance. "
               "Trump faced impeachment twice by the House of Representatives, first for his involvement with Ukraine "
               "and, after leaving office, for his alleged role in inciting an insurrection at the U.S. Capitol "
               "on January 6, 2021."
    ),
    DocumentGenerationTaskExample(
        subject="Zinedine Zidane",
        format="Football player biography",
        expected_contents=["Date of birth", "Club teams", "National team", "Position"],
        output="Zinedine Zidane, born June 23, 1972, in Marseille, France, "
               "is a former professional footballer and renowned manager. "
               "As a midfielder, he played for clubs like AS Cannes, Girondins de Bordeaux, "
               "Juventus, and Real Madrid, achieving notable success. "
               "Internationally, he represented France, winning the 1998 FIFA World Cup "
               "and the 2000 UEFA European Championship. "
               "In 2006, an infamous headbutt marked his final player appearance in the World Cup final."
    ),
    DocumentGenerationTaskExample(
        subject="Nick Manton",
        format="Football player biography",  # Nick Manton is not a football player
        expected_contents=["Date of birth", "Club teams", "National team", "Position"],
        output=None
    ),
    DocumentGenerationTaskExample(
        subject="London",
        format="City factsheet",
        expected_contents=["Country", "Population", "Industries", "Important historical events"],
        output="London, the capital city of the United Kingdom, boasts a population of approximately 9 million. "
               "Its temperate maritime climate experiences mild temperatures and moderate rainfall "
               "throughout the year. As a global financial hub, London's economy centers on "
               "banking, finance, and a range of industries. "
               "Historically, significant events include the Norman conquest of 1066, the Great Fire of 1666, "
               "and the Blitz during World War II."
    ),
    DocumentGenerationTaskExample(
        subject="Africa",
        format="City factsheet",  # Africa is not a city
        expected_contents=["Country", "Population", "Industries", "Important historical events"],
        output=None
    ),
]


class OpenAIDocumentGenerator(AbstractDocumentGenerator):
    """A document generator relying purely on ChatGPT. No Google/Wikipedia search is used."""

    def __init__(self) -> None:
        self._chat_handler = OpenAIChatHandler()

    def generate(self, subject: str, format: str, expected_contents: Iterable[str]) -> Optional[str]:
        prompt = self._construct_prompt(subject, format, expected_contents)
        response = self._chat_handler.run(prompt)
        return self._parse_response(response, subject)

    @staticmethod
    def _construct_prompt(subject: str, format: str, expected_contents: Iterable[str]) -> list[ChatMessage]:
        messages: list[ChatMessage] = []

        messages.append(SystemMessage(content=SYSTEM_MESSAGE))

        for example in EXAMPLES:
            messages.append(UserMessage(
                content=construct_user_message(example.subject, example.format, example.expected_contents)
            ))
            messages.append(AssistantMessage(
                content=construct_assistant_message(example.output)
            ))

        messages.append(UserMessage(
            content=construct_user_message(subject, format, expected_contents)
        ))

        return messages

    @staticmethod
    def _parse_response(response: AssistantMessage, subject: str) -> Optional[str]:
        document = parse_assistant_message(response.content, subject)
        return document
