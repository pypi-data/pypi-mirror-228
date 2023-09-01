import pytest

from chemchef.agent.agent import Agent
from chemchef.agent.agent_responses import ParsedAssistantMessage, ParsedAssistantMessageForTool, \
    ParsedAssistantMessageForFinalAnswer
from chemchef.agent.tools import AbstractTool
import logging
logging.basicConfig(level=logging.INFO)


class BrownFamilyTool(AbstractTool):
    NAME = "Brown Family Member Biography Lookup"

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def description(self) -> str:
        return "Given the first name of a member of the fictional Brown family, returns a biography of that family member."

    @property
    def input_format_description(self) -> str:
        return "first name of Brown family member"

    def run(self, input_text: str) -> str:
        name = input_text
        if name == "Jane":
            return "Name: Jane\nAge: 21"
        elif name == "Mary":
            return "Name: Mary\nAge: 17"
        else:
            return f"{name} is not a member of the Brown family"


TOOLS: list[AbstractTool] = [BrownFamilyTool()]

EXAMPLES: list[ParsedAssistantMessage] = [
    ParsedAssistantMessageForTool(
        question='Is Elizabeth Brown legally allowed to start driving lessons in the UK?',
        knowledge='To start driving lessons in the UK, you have to be at least 16 years old.',
        plan="Look up Elizabeth Brown's biography and extract her age. "
             "Determine if she is old enough to take driving lessons.",
        tool_name=BrownFamilyTool.NAME,
        tool_input="Elizabeth"
    ),
    ParsedAssistantMessageForFinalAnswer(
        question='Is Elizabeth Brown legally allowed to start driving lessons in the UK?',
        knowledge='To take driving lessons in the UK, you have to be at least 16 years old. '
                  'Elizabeth Brown is 18 years old, so she is legally allowed to start driving lessons in the UK.',
        plan="No further steps",
        answer="Yes, Elizabeth Brown is legally allowed to start driving lessons in the UK, since "
               "she is 18 years old, while the minimum age to take driving lessons is only 16 years."
    ),
]


def run(tools: list[AbstractTool], examples: list[ParsedAssistantMessage], question: str,
        must_contain_at_least_one: set[str]) -> None:
    print(f"Question: {question}")

    agent = Agent(tools=tools, assistant_message_examples=examples)
    answer = agent.run(question)

    print(f"Answer: {answer}")

    words_in_answer = {word.lower() for word in answer.split()}
    assert any(expected_word.lower() in words_in_answer for expected_word in must_contain_at_least_one)


@pytest.mark.flaky(reruns=3)
def test_simple_case() -> None:
    run(
        tools=TOOLS,
        examples=EXAMPLES,
        question="Jane and Mary are two members of the fictional Brown family. "
                 "What is the age difference between Jane and Mary?",
        must_contain_at_least_one={"four", "4"}
    )
