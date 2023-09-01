import logging

from chemchef.agent.agent_responses import ParsedAssistantMessage, construct_assistant_message, FORMATTING_INSTRUCTION, \
    parse_assistant_message, ParsedAssistantMessageForTool, ParsedAssistantMessageForFinalAnswer
from chemchef.agent.tools import AbstractTool, ToolUsageError
from chemchef.clients.openai import ChatMessage, SystemMessage, UserMessage, OpenAIChatHandler, AssistantMessage

SYSTEM_MESSAGE_SKELETON = "In this conversation, the AI assistant is helping the user to find the answer to a question. "\
                 "While it is possible that the AI assistant may already know the answer to the question, "\
                 "it is more likely that getting to the answer will a multi-step process, involving the use of "\
                 "one or more tools along the way to obtain relevant information. "\
                 "The AI assistant is particularly skilled at breaking down a complex problem into a series of "\
                 "more manageable sub-problems that can reasonably be solved using the tools available, and "\
                 "will often find indirect strategies to tackle a problem when the most direct strategy "\
                 "is ineffective. \n\n\n"\
                 "**OVERALL STRUCTURE OF CONVERSATION:**\n\n"\
                 "The conversation begins with the user posing the question. "\
                 "From here on, the AI assistant has two options:\n"\
                 "1. The AI assistant can recommend that the user should use one of the available tools "\
                 "to retrieve additional information relevant to the user's question. "\
                 "The user will then respond with the information obtained by using that tool. "\
                 "The conversation pattern then repeats.\n" \
                 "2. Alternatively, if the AI assistant already has enough knowledge at its disposal, "\
                 "then it can provide the final answer to the question. This ends the conversation.\n\n\n" \
                 "**AVAILABLE TOOLS:**\n\n{}\n\n\n"\
                 f"**FORMAT OF AI ASSISTANT MESSAGES:**\n\n{FORMATTING_INSTRUCTION}\n\n\n"\
                 "**EXAMPLE AI ASSISTANT MESSAGES:**\n\n{}\n\n"\
                 "It is essential that the AI assistant adheres strictly to the message formats "\
                 "as laid out in the examples above."

TOOL_DESCRIPTION = "- {}: {} [Expected input format: {}]"


def _construct_tool_descriptions(tools: list[AbstractTool]) -> str:
    description_lines: list[str] = []
    for tool in tools:
        description_lines.append(TOOL_DESCRIPTION.format(
            tool.name, tool.description, tool.input_format_description))
    return '\n'.join(description_lines)


def _construct_assistant_message_examples(examples: list[ParsedAssistantMessage]) -> str:
    return '\n\n...OR...\n\n'.join(construct_assistant_message(example) for example in examples)


def _construct_system_message(tools: list[AbstractTool], examples: list[ParsedAssistantMessage]) -> str:
    return SYSTEM_MESSAGE_SKELETON.format(
        _construct_tool_descriptions(tools),
        _construct_assistant_message_examples(examples)
    )


def _get_tool_from_name(tool_name: str, tools: list[AbstractTool]) -> AbstractTool:
    for tool in tools:
        if tool.name == tool_name:
            return tool

    # invalid name:
    raise ToolUsageError(f"{tool_name} is not a valid tool name. "
                         f"Valid tool names are {', '.join(tool.name for tool in tools)}")


class Agent:

    def __init__(self, tools: list[AbstractTool], assistant_message_examples: list[ParsedAssistantMessage]):
        self._tools = tools
        self._assistant_message_examples = assistant_message_examples

    def run(self, question: str) -> str:
        handler = OpenAIChatHandler()

        logging.info("Question\n%s\n", question)
        message_history: list[ChatMessage] = [
            SystemMessage(content=_construct_system_message(self._tools, self._assistant_message_examples)),
            UserMessage(content=question)
        ]

        while True:
            response = handler.run(message_history)

            logging.info("Agent thoughts:\n%s\n", response.content)
            assert isinstance(response, AssistantMessage)
            message_history.append(response)

            try:
                parsed_agent_response = parse_assistant_message(response.content)

                if isinstance(parsed_agent_response, ParsedAssistantMessageForTool):
                    tool = _get_tool_from_name(parsed_agent_response.tool_name, self._tools)
                    input_to_tool = parsed_agent_response.tool_input

                    output_from_tool = tool.run(input_to_tool)

                    logging.info("Tool output:\n%s\n", output_from_tool)
                    message_history.append(UserMessage(content=output_from_tool))

                elif isinstance(parsed_agent_response, ParsedAssistantMessageForFinalAnswer):
                    final_answer = parsed_agent_response.answer

                    logging.info("Final answer:%s\n\n", final_answer)
                    return final_answer

            except ToolUsageError as ex:
                logging.error("%s\n", str(ex))
                message_history.append(UserMessage(content=f"ERROR: {str(ex)}"))

