import json

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage
import os
import trafilatura

MODEL_NAME = "gpt-5-nano"


def get_model():
    return init_chat_model(MODEL_NAME)


def get_messages(data, additional_info):
    system_msg = SystemMessage(
        "Turn this document into a maximally concise document. The goal is to create a document that can be later on by an anki card creation as a reference:")
    human_msg = HumanMessage(data)

    messages = [system_msg] + (
        [
            SystemMessage(f"Additionally consider {additional_info}")
        ] if additional_info != "" else []
    ) + [human_msg]

    return messages
