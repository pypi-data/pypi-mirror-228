from typing import NamedTuple, Union

from chemchef.agent.tools import ToolUsageError, GoogleSearchTool, QuestionAnsweringFromWebPageTool


class ParsedAssistantMessageForTool(NamedTuple):
    question: str  # "Original question"
    knowledge: str  # "Current knowledge/experience"
    plan: str  # "Plan going forward"
    tool_name: str  # "Next tool"
    tool_input: str  # "Input to next tool"


class ParsedAssistantMessageForFinalAnswer(NamedTuple):
    question: str  # "Original question"
    knowledge: str  # "Current knowledge/experience"
    plan: str  # "Plan going forward"
    answer: str  # "Final answer"


ParsedAssistantMessage = Union[ParsedAssistantMessageForTool, ParsedAssistantMessageForFinalAnswer]


QUESTION_HEADER = "Original question: "
KNOWLEDGE_HEADER = "Cumulative knowledge/experience: "
PLAN_HEADER = "Plan going forward: "
TOOL_NAME_HEADER = "Next tool: "
TOOL_INPUT_HEADER = "Input to next tool: "
ANSWER_HEADER = "Final answer: "


FORMAT_DESCRIPTION = f"either a five-line response (with lines beginning with '{QUESTION_HEADER}', '{KNOWLEDGE_HEADER}', '{PLAN_HEADER}', '{TOOL_NAME_HEADER}' and '{TOOL_INPUT_HEADER}') " + \
                     f"or a four-line response (with lines beginning with '{QUESTION_HEADER}', '{KNOWLEDGE_HEADER}', '{PLAN_HEADER}' and '{ANSWER_HEADER}') "

PARSING_ERROR_MESSAGE = f"I am expecting {FORMAT_DESCRIPTION}."


def construct_assistant_message(structured_message: ParsedAssistantMessage) -> str:
    if isinstance(structured_message, ParsedAssistantMessageForTool):
        return f"{QUESTION_HEADER}{structured_message.question}\n"\
               f"{KNOWLEDGE_HEADER}{structured_message.knowledge}\n"\
               f"{PLAN_HEADER}{structured_message.plan}\n"\
               f"{TOOL_NAME_HEADER}{structured_message.tool_name}\n"\
               f"{TOOL_INPUT_HEADER}{structured_message.tool_input}"
    elif isinstance(structured_message, ParsedAssistantMessageForFinalAnswer):
        return f"{QUESTION_HEADER}{structured_message.question}\n"\
               f"{KNOWLEDGE_HEADER}{structured_message.knowledge}\n"\
               f"{PLAN_HEADER}{structured_message.plan}\n"\
               f"{ANSWER_HEADER}{structured_message.answer}"
    else:
        raise ValueError


def parse_assistant_message(message: str) -> ParsedAssistantMessage:
    lines = [line.strip() for line in message.splitlines() if len(line.strip()) > 0]

    if len(lines) == 5:
        question = _extract_from_line(lines[0], QUESTION_HEADER)
        knowledge = _extract_from_line(lines[1], KNOWLEDGE_HEADER)
        plan = _extract_from_line(lines[2], PLAN_HEADER)
        tool_name = _extract_from_line(lines[3], TOOL_NAME_HEADER)
        tool_input = _extract_from_line(lines[4], TOOL_INPUT_HEADER)

        return ParsedAssistantMessageForTool(
            question=question,
            knowledge=knowledge,
            plan=plan,
            tool_name=tool_name,
            tool_input=tool_input
        )

    elif len(lines) == 4:
        question = _extract_from_line(lines[0], QUESTION_HEADER)
        knowledge = _extract_from_line(lines[1], KNOWLEDGE_HEADER)
        plan = _extract_from_line(lines[2], PLAN_HEADER)
        answer = _extract_from_line(lines[3], ANSWER_HEADER)

        return ParsedAssistantMessageForFinalAnswer(
            question=question,
            knowledge=knowledge,
            plan=plan,
            answer=answer
        )

    else:
        raise ToolUsageError(PARSING_ERROR_MESSAGE)


def _extract_from_line(line: str, expected_header: str) -> str:
    if not line.startswith(expected_header):
        raise ToolUsageError(PARSING_ERROR_MESSAGE)

    line_without_header = line[len(expected_header):]
    return line_without_header.strip()


TEMPLATE_TOOL_MESSAGE = ParsedAssistantMessageForTool(
    question="[A restatement of the user's original question]",
    knowledge="[Up to five sentences summarising relevant knowledge the agent had prior to the tools being used, plus "
              "relevant knowledge accumulated from usage of the tools thus far. This summary must "
              "describe *all* of the accumulated knowledge, not just the knowledge gained from the "
              "most recently-used tool. If no tools have been used as of yet,"
              "then this summary should solely focus on the agent's prior knowledge.]",
    plan="[Up to five sentences describing the agent's plan for how to arrive at an answer to the user's question "
         "using the tools available. This should demonstrate awareness of how to break down the complex problem into "
         "a series of more manageable steps that can realistically be solved using the tools available.]",
    tool_name="[The name of the tool to use next]",
    tool_input="[The input to the tool]"
)


TEMPLATE_FINAL_ANSWER_MESSAGE = ParsedAssistantMessageForFinalAnswer(
    question="[A restatement of the user's original question]",
    knowledge="[Up to five sentences summarising relevant knowledge the agent had prior to the tools being used, plus "
              "relevant knowledge accumulated from usage of the tools thus far. This summary must "
              "describe *all* of the accumulated knowledge, not just the knowledge gained from the "
              "most recently-used tool. If no tools have been used as of yet,"
              "then this summary should solely focus on the agent's prior knowledge.]",
    plan="[Should say 'No further steps', since the agent is ready to provide a final answer.]",
    answer="[One or two sentences that answer to the user's original question in a helpful manner]"
)


FORMATTING_INSTRUCTION = f"Each AI assistant message must be formatted as {FORMAT_DESCRIPTION}. "\
                         f"In other words, the correct format is:\n\n{construct_assistant_message(TEMPLATE_TOOL_MESSAGE)}\n\n"\
                         f"...OR...\n\n{construct_assistant_message(TEMPLATE_FINAL_ANSWER_MESSAGE)}"


STANDARD_ASSISTANT_MESSAGE_EXAMPLES: list[ParsedAssistantMessage] = [
    ParsedAssistantMessageForTool(
        question='Who won the Oscar for best actor in 2022?',
        knowledge='Wikipedia is a dependable source for this kind of information.',
        plan='Run a Google search to find the URL for the relevant Wikipedia page. '
             'Extract the information from this Wikipedia page.',
        tool_name=GoogleSearchTool.NAME,
        tool_input="oscar best actor 2022 wikipedia"
    ),
    ParsedAssistantMessageForTool(
        question='Who won the Oscar for best actor in 2022?',
        knowledge='The wikipedia article https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor is likely to list '
                  'the winners of the award in each year.',
        plan='Extract the information from this Wikipedia page.',
        tool_name=QuestionAnsweringFromWebPageTool.NAME,
        tool_input="Who won the Oscar for best actor in 2022? https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor"
    ),
    ParsedAssistantMessageForFinalAnswer(
        question='Who won the Oscar for best actor in 2022?',
        knowledge='Will Smith won the Oscar for best actor in 2022',
        plan='No further steps',
        answer='Will Smith'
    ),
    ParsedAssistantMessageForTool(
        question='Which smartphones have a longer battery life than the iPhone 11?',
        knowledge='The iPhone 11 is a recent smartphone. Samsung Galaxy and Google Pixel are popular competitors.',
        plan='Find a web page that compares the battery lives of different phones, '
             'including the iPhone 11, the Samsung Galaxy and the Google Pixel, and extract the relevant information ',
        tool_name=GoogleSearchTool.NAME,
        tool_input="phone battery life comparison iPhone 11 Samsung Google Pixel"
    ),
    ParsedAssistantMessageForTool(
        question="Which batter in the England men's cricket team scored the highest individual score in a Test match in 2023?",
        knowledge="It is unlikely that any web page will answer the question directly. "
                  "However, the ECB website should list the current Test squad, "
                  "and Cricinfo should have information about each player's scores in individual matches",
        plan='Find the page on the ECB website that lists the current Test squad, and extract the list of names. '
             'For each squad member who is a top order batter, '
             'look up the runs scored by that player in Test innings in 2023 on Cricinfo.',
        tool_name=GoogleSearchTool.NAME,
        tool_input="ecb cricket men Test squad"
    ),
    ParsedAssistantMessageForTool(
        question="Which batter in the England men's cricket team scored the highest individual score in a Test match in 2023?",
        knowledge="Zak Crawley, Ben Duckett, Ben Stokes, Jonny Bairstow and Harry Brook are "
                  "the top order batters in the England Test squad. "
                  "In 2023, Zak Crawley's highest Test score was 156, while Ben Duckett's highest Test score was 187.",
        plan='Look up the runs scored by Ben Stokes in Test innings in 2023 on Cricinfo. '
             'Then repeat for Jonny Bairstow and Harry Brook',
        tool_name=GoogleSearchTool.NAME,
        tool_input="Ben Stokes cricinfo"
    ),
    ParsedAssistantMessageForTool(
        question="Which batter in the England men's cricket team scored the highest individual score in a Test match in 2023?",
        knowledge="Zak Crawley, Ben Duckett, Ben Stokes, Jonny Bairstow and Harry Brook are "
                  "the top order batters in the England Test squad. "
                  "In 2023, Zak Crawley's highest Test score was 156, while Ben Duckett's highest Test score was 187. "
                  "Ben Stoke's Test scores in 2023 should be on https://www.espncricinfo.com/cricketers/ben-stokes-311158",
        plan='Look up the runs scored in individual Test matches in 2023 by Ben Stokes on Cricinfo - can use the above URL. '
             'Then repeat for Jonny Bairstow and Harry Brook',
        tool_name=QuestionAnsweringFromWebPageTool.NAME,
        tool_input="What is Ben Stokes' highest innings score as a Test batter in 2023? https://www.espncricinfo.com/cricketers/ben-stokes-311158"
    ),
    ParsedAssistantMessageForFinalAnswer(
        question="Which batter in the England men's cricket team scored the highest individual score in a Test match in 2023?",
        knowledge="Zak Crawley, Ben Duckett, Ben Stokes, Jonny Bairstow and Harry Brook are "
                  "the top order batters in the England Test squad. "
                  "In 2023, the highest test scores for these players are 156 for Zak Crawley, 187 for Ben Duckett, "
                  "79 for Ben Stokes, 142 for Jonny Bairstow and 250 for Harry Brook. "
                  "Therefore, Harry Brook scored the highest individual score in a Test match in 2023.",
        plan='No further steps',
        answer='Harry Brook - highest Test innings score in 2023 is 250'
    ),
    ParsedAssistantMessageForFinalAnswer(
        question='What is the capital of Spain?',
        knowledge='Madrid is the capital of Spain. (This is common knowledge - no tools are required,)',
        plan='No further steps',
        answer='Madrid'
    ),
]
