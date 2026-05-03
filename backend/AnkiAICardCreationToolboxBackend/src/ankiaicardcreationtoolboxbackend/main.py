"""FastAPI application for Anki AI card creation."""

import os
from contextlib import suppress
from threading import Lock, Timer

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ankiaicardcreationtoolboxbackend.agent import get_agent_response

app = FastAPI()
RATE_LIMIT_WINDOW_SECONDS = 10 * 60
_rate_limit_window_lock = Lock()

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


def _release_rate_limit_lock() -> None:
    """Release the cooldown lock if it is currently held."""
    with suppress(RuntimeError):
        _rate_limit_window_lock.release()


def clear_rate_limit_state() -> None:
    """Clear in-memory rate-limit state."""
    _release_rate_limit_lock()


def _enforce_rate_limit() -> None:
    """Allow only one request within the configured time window per process."""
    if not _rate_limit_window_lock.acquire(blocking=False):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later.",
            headers={"Retry-After": str(RATE_LIMIT_WINDOW_SECONDS)},
        )

    release_timer = Timer(RATE_LIMIT_WINDOW_SECONDS, _release_rate_limit_lock)
    release_timer.daemon = True
    release_timer.start()


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
