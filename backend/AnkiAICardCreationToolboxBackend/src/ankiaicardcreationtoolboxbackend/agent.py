"""Agent module for creating and invoking the Anki card creation agent."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from deepagents import create_deep_agent

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable

from ankiaicardcreationtoolboxbackend.tools import anki_formatting_guidelines, best_practices_of_formulating_knowledge

DEFAULT_AGENT_MODEL = "openai:gpt-5.2"
_model_override = os.environ.get("OPENAI_MODEL_OVERRIDE")
AGENT_MODEL = f"openai:{_model_override}" if _model_override else DEFAULT_AGENT_MODEL


def create_agent() -> Runnable:
    """Create the Anki card creation agent with knowledge base tools.

    Returns:
        A configured LangChain runnable agent.
    """
    return create_deep_agent(
        tools=[best_practices_of_formulating_knowledge, anki_formatting_guidelines],
        system_prompt="""
        You are an Anki Card Creator. Your sole task is to generate Anki cards from the user's input.
        Apply best practices of formulating knowledge and Anki formatting guidelines when creating the cards.
        You must ONLY output the Anki cards themselves — nothing else.
        Do NOT ask questions, do NOT request clarifications, do NOT add introductions, explanations,
        commentary, or any text that is not part of the cards.
        If the input is insufficient, still generate the best possible cards from what is given.
        """.strip(),
        model=AGENT_MODEL,
    )


def get_agent_response(text: str) -> str:
    """Invoke the agent and return its text response.

    Args:
        text: The user input text to generate cards from.

    Returns:
        The agent's generated card content as a string.
    """
    result = create_agent().invoke({"messages": [{"role": "user", "content": text}]})
    return result["messages"][-1].content[0]["text"]
