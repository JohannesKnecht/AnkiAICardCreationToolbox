"""LangChain model and message construction for knowledge base creation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel
    from langchain_core.messages import BaseMessage

MODEL_NAME = "gpt-5-nano"


def get_model() -> BaseChatModel:
    """Return the chat model used for knowledge base summarisation.

    Returns:
        An initialised chat model instance.
    """
    return init_chat_model(MODEL_NAME)


def get_messages(data: str, additional_info: str) -> list[BaseMessage]:
    """Build the message list for the knowledge base summarisation chain.

    Args:
        data: The extracted text content from the web source.
        additional_info: Extra instructions to include in the system prompt.

    Returns:
        A list of messages to send to the chat model.
    """
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
