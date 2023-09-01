import logging
from typing import Iterable

from chemchef.agent.summarization.chunking import to_chunks
from chemchef.clients.openai import ChatMessage, SystemMessage, UserMessage, OpenAIChatHandler

SYSTEM_MESSAGE = "The AI assistant is helping the human user to answer a question using information in a text. "

USER_MESSAGE_INIT = "I want to answer the following question.\n\nQUESTION: {}\n\n"\
                    "I have a text that may contain information is that useful for answering this question. "\
                    "Below is the opening section of a text. "\
                    "Write a summary of this section of text, containing any information in the text "\
                    "that is relevant to answering my question. "\
                    "Your summary should include information that directly answers my question, "\
                    "and information that is indirectly relevant, and "\
                    "pointers to other sources that may be relevant for answering my question. "\
                    "Your summary should be as concise as possible (and definitely under 200 words). "\
                    "Your summary should give prominence to the points that are most relevant to the question, "\
                    "while omitting information that is irrelevant to the question. " \
                    "Your summary should include a sentence that describes whether or not the text appears to be "\
                    "reliable and appropriate for the task at hand. " \
                    "If the text contains nothing of relevance to my question, then return an empty summary.\n\n "\
                    "TEXT: {}"

USER_MESSAGE_CONT = "I want to answer the following question.\n\nQUESTION: {}\n\n" \
                    "I have a text that may contain information is that useful for answering this question. " \
                    "You are writing a summary of the text. "\
                    "You are doing this by processing one section of the text at a time, "\
                    "revising your summary as you go. "\
                    "You have already processed the opening sections of the text. "\
                    "Here is the summary that you have built up so far.\n\nEXISTING SUMMARY: {}\n\n"\
                    "Below is the next section of this text. "\
                    "Write a revised version of your summary, which combines the information in your existing summary "\
                    "with any additional information from the current section of the text that is relevant "\
                    "to answering my question. "\
                    "Your summary should include information that directly answers my question, "\
                    "and information that is indirectly relevant, and "\
                    "pointers to other sources that may be relevant to answering my question. "\
                    "Your revised summary should be as concise as possible  (and definitely under 200 words). "\
                    "Your revised summary should give prominence to the points that are most relevant to the question, "\
                    "while omitting information that is irrelevant to the question. "\
                    "Your revised summary should include a sentence that describes whether or not the text appears to be "\
                    "reliable and appropriate for the task at hand. " \
                    "Your summary should read as if it is a unified summary of the text up to the current section - "\
                    "it should not make reference to 'prior sections'/'previous sections' "\
                    "or the 'current section'/'this section'."\
                    "If the current section of the text contains nothing of relevance to my question, "\
                    "then just return your existing summary in its current state.\n\n"\
                    "TEXT: {}"


USER_MESSAGE_FINAL = "I want to answer the following question.\n\nQUESTION: {}\n\n" \
                    "I have a text that may contain information is that useful for answering this question. " \
                    "You have been writing a summary of the text. "\
                    "You were doing this by processing one section of the text at a time, "\
                    "revising your summary as you go. "\
                    "Here is the summary that you built up in this manner.\n\nSUMMARY: {}\n\n"\
                    "Using this summary, write an answer to my original question. "\
                    "Structure your answer according to the format below:\n\n"\
                    "Answer to question: [One or two sentences that directly answer my original question, "\
                    "using information from the summary provided. "\
                    "(If there is not enough information in the summary to "\
                    "directly answer my original question, then say so.)]\n"\
                    "Other information of relevance: (Optional) [One or two sentences that provide information "\
                    "that constitutes partial progress towards answering my question. (Do not include information "\
                    "that is irrelevant to my question though.)]\n"\
                    "Criticism of the source: [One or two sentences raising any concerns you may have about the"\
                    "reliability or appropriateness of the text, plus advice about how to find texts that are more "\
                    "reliable or better suited to answering my question.]"


def summarise(question: str, text: str,
              chunk_size: int = 3000, overlap_size: int = 250, max_chunks: int = 5) -> str:
    return summarise_from_chunks(question, to_chunks(text, chunk_size, overlap_size, max_chunks))


def summarise_from_chunks(question: str, text_chunks: Iterable[str]) -> str:
    handler = OpenAIChatHandler()

    summary_so_far: str = ""

    for chunk_id, chunk in enumerate(text_chunks):
        prompts: list[ChatMessage] = [
            SystemMessage(content=SYSTEM_MESSAGE)
        ]

        if len(summary_so_far) == 0:
            prompts.append(UserMessage(content=USER_MESSAGE_INIT.format(question, chunk)))
        else:
            prompts.append(UserMessage(content=USER_MESSAGE_CONT.format(question, summary_so_far, chunk)))

        response = handler.run(prompts)
        summary_so_far = _strip_headers_in_response(response.content)

        logging.info("Summary extracted from first %s chunks of web page: %s\n", chunk_id + 1, summary_so_far)

    # Finalising
    prompts = [
        SystemMessage(content=SYSTEM_MESSAGE),
        UserMessage(content=USER_MESSAGE_FINAL.format(question, summary_so_far))
    ]

    response = handler.run(prompts)
    return _remove_empty_lines(_strip_headers_in_response(response.content))


def _strip_headers_in_response(response: str) -> str:
    possible_headers = ['SUMMARY: ', 'REVISED SUMMARY: ', 'EXISTING SUMMARY: ', 'ANSWER: ']
    for header in possible_headers:
        if response.startswith(header):
            return response[len(header):]

    # default: no header to remove
    return response


def _remove_empty_lines(response: str) -> str:
    lines = [line.strip() for line in response.splitlines() if len(line.strip()) > 0]
    return '\n'.join(lines)
