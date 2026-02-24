import os

from fastapi import FastAPI
from deepagents import create_deep_agent
from pydantic import BaseModel

from ankiaicardcreationtoolboxbackend.tools import best_practices_of_formulating_knowledge

app = FastAPI()


class CardRequestData(BaseModel):
    text: str


@app.post("/create_cards")
async def create_cards(card_request_data: CardRequestData):
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not set")

    agent = create_deep_agent(
        tools=[best_practices_of_formulating_knowledge],
        system_prompt="You are an Anki Card Creator. Given the input of the user apply best practices and return good cards.",
        model="openai:gpt-5.2"
    )

    # Run the agent
    result = agent.invoke(
        {"messages": [{"role": "user", "content": card_request_data.text}]}
    )

    return result["messages"][-1].content[0]["text"]
