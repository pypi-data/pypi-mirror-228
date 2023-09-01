import openai
from pydantic import BaseModel
from enum import Enum
from abc import ABC, abstractmethod


class StrEnum(str, Enum):
    def __repr__(self) -> str:
        return str.__repr__(self.value)


class ChatRole(StrEnum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"


class ChatMessage(BaseModel):
    role: ChatRole
    content: str


class SystemMessage(ChatMessage):
    role: ChatRole = ChatRole.SYSTEM


class AssistantMessage(ChatMessage):
    role: ChatRole = ChatRole.ASSISTANT


class UserMessage(ChatMessage):
    role: ChatRole = ChatRole.USER


class AbstractChatHandler(ABC):

    @abstractmethod
    def run(self, prompts: list[ChatMessage]) -> ChatMessage:
        raise NotImplementedError


class OpenAIChatHandler(AbstractChatHandler):

    def run(self, prompts: list[ChatMessage]) -> AssistantMessage:
        json_messages = [message.dict() for message in prompts]
        response = openai.ChatCompletion.create(  # type: ignore
            model="gpt-4",
            messages=json_messages
        )
        return AssistantMessage(**response["choices"][0]["message"])
