from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


MODEL_NAME = "gpt-5-nano"


def get_model() -> BaseChatModel:
    return init_chat_model(MODEL_NAME)


def get_messages(data: str, additional_info: str) -> list[BaseMessage]:
    system_msg = SystemMessage(
        """
        Turn this document into a maximally concise document.
        The goal is to create a document that can be later on by an anki card creation as a reference.
        You are not allowed to ask questions. Only respond with the document:
        """.strip()
    )
    human_msg = HumanMessage(data)

    messages = (
        [system_msg]
        + ([SystemMessage(f"Additionally consider {additional_info}")] if additional_info != "" else [])
        + [human_msg]
    )

    return messages
