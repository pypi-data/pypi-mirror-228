from chemchef.clients.openai.chatgpt_client import OpenAIChatHandler, SystemMessage, UserMessage, ChatRole


def test_run() -> None:
    client = OpenAIChatHandler()
    response = client.run([
        SystemMessage(content="This is a conversation between a human user and a friendly AI assistant."),
        UserMessage(content="Please tell me what I can do in London during the weekend.")
    ])
    assert response.role == ChatRole.ASSISTANT
    assert len(response.content) >= 1
