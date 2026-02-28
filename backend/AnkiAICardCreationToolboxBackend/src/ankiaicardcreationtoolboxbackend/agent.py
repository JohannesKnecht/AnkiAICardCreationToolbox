import os
from typing import Any

from fastapi import FastAPI
from deepagents import create_deep_agent

from ankiaicardcreationtoolboxbackend.tools import best_practices_of_formulating_knowledge, anki_formatting_guidelines

DEFAULT_AGENT_MODEL = "openai:gpt-5.2"
_model_override = os.environ.get("OPENAI_MODEL_OVERRIDE")
AGENT_MODEL = f"openai:{_model_override}" if _model_override else DEFAULT_AGENT_MODEL


def create_agent() -> Any:
    return create_deep_agent(
        tools=[
            best_practices_of_formulating_knowledge,
            anki_formatting_guidelines],
        system_prompt="""
        You are an Anki Card Creator. Given the input of the user apply best practices and return good cards.
        You are not allowed to ask questions. Only respond with the document
        """.strip(),
        model=AGENT_MODEL
    )


def get_agent_response(text: str) -> str:
    result = create_agent().invoke(
        {"messages": [{"role": "user", "content": text}]}
    )
    return result["messages"][-1].content[0]["text"]
