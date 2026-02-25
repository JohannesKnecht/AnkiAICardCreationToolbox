from fastapi import FastAPI
from deepagents import create_deep_agent

from ankiaicardcreationtoolboxbackend.tools import best_practices_of_formulating_knowledge, anki_formatting_guidelines


def create_agent():
    return create_deep_agent(
        tools=[
            best_practices_of_formulating_knowledge,
            anki_formatting_guidelines],
        system_prompt="You are an Anki Card Creator. Given the input of the user apply best practices and return good cards.",
        model="openai:gpt-5.2"
    )


def get_agent_response(text):
    result = create_agent().invoke(
        {"messages": [{"role": "user", "content": text}]}
    )
    return result["messages"][-1].content[0]["text"]
