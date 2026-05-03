"""FastAPI application for Anki AI card creation."""

import os
from math import ceil
from threading import Lock
from time import monotonic

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ankiaicardcreationtoolboxbackend.agent import get_agent_response

app = FastAPI()
RATE_LIMIT_WINDOW_SECONDS = 10 * 60
_rate_limit_state = {"last_request_time": None}
_rate_limit_lock = Lock()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://f618ad7356200906-frontend-service-y55vgiciiq-uc.a.run.app",
]

app.add_middleware(
    CORSMiddleware,  # type: ignore[invalid-argument-type]
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CardRequestData(BaseModel):
    """Request body for the card creation endpoint."""

    text: str


def resource_check() -> None:
    """Verify that required environment variables are set."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")


def clear_rate_limit_state() -> None:
    """Clear in-memory rate-limit state."""
    with _rate_limit_lock:
        _rate_limit_state["last_request_time"] = None


def _enforce_rate_limit() -> None:
    """Allow only one request within the configured time window per process."""
    now = monotonic()

    with _rate_limit_lock:
        last_request_time = _rate_limit_state["last_request_time"]
        if last_request_time is not None:
            remaining_seconds = last_request_time + RATE_LIMIT_WINDOW_SECONDS - now
            if remaining_seconds > 0:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Try again later.",
                    headers={"Retry-After": str(ceil(remaining_seconds))},
                )

        _rate_limit_state["last_request_time"] = now


@app.post("/create_cards")
async def create_cards(card_request_data: CardRequestData) -> str:
    """Create Anki cards from the provided text.

    Args:
        card_request_data: The request body containing the text to create cards from.

    Returns:
        The generated Anki cards as a string.
    """
    resource_check()
    _enforce_rate_limit()

    text = card_request_data.text
    if len(text) > 1000:
        raise HTTPException(status_code=400, detail="text too long")

    return get_agent_response(text)
