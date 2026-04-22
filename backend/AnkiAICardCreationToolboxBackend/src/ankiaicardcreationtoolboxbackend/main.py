"""FastAPI application for Anki AI card creation."""

import os
from math import ceil
from threading import Lock
from time import monotonic

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ankiaicardcreationtoolboxbackend.agent import get_agent_response

app = FastAPI()
RATE_LIMIT_WINDOW_SECONDS = 10 * 60
RATE_LIMIT_CLEANUP_EVERY_REQUESTS = 100
_last_request_time_per_ip: dict[str, float] = {}
_rate_limit_lock = Lock()
_request_counter = 0

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
        global _request_counter  # noqa: PLW0603
        _last_request_time_per_ip.clear()
        _request_counter = 0


def _get_client_ip(request: Request) -> str:
    """Extract the most relevant client IP for rate limiting."""
    trust_forwarded_for = os.environ.get("TRUST_X_FORWARDED_FOR", "").lower() in {"1", "true", "yes"}
    if trust_forwarded_for:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _enforce_rate_limit(request: Request) -> None:
    """Allow only one request per IP within the configured time window.

    This is an in-memory, per-process limit intended as a basic safeguard.
    """
    client_ip = _get_client_ip(request)
    now = monotonic()

    with _rate_limit_lock:
        global _request_counter  # noqa: PLW0603
        _request_counter += 1
        if _request_counter % RATE_LIMIT_CLEANUP_EVERY_REQUESTS == 0:
            expiration_cutoff = now - RATE_LIMIT_WINDOW_SECONDS
            active_entries = {
                ip: last_request_time
                for ip, last_request_time in _last_request_time_per_ip.items()
                if last_request_time >= expiration_cutoff
            }
            _last_request_time_per_ip.clear()
            _last_request_time_per_ip.update(active_entries)

        last_request_time = _last_request_time_per_ip.get(client_ip)
        if last_request_time is not None and now - last_request_time < RATE_LIMIT_WINDOW_SECONDS:
            retry_after_seconds = ceil(RATE_LIMIT_WINDOW_SECONDS - (now - last_request_time))
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Try again later.",
                headers={"Retry-After": str(retry_after_seconds)},
            )
        _last_request_time_per_ip[client_ip] = now


@app.post("/create_cards")
async def create_cards(card_request_data: CardRequestData, request: Request) -> str:
    """Create Anki cards from the provided text.

    Args:
        card_request_data: The request body containing the text to create cards from.
        request: The incoming HTTP request used for rate limiting.

    Returns:
        The generated Anki cards as a string.
    """
    _enforce_rate_limit(request)
    resource_check()

    text = card_request_data.text
    if len(text) > 1000:
        raise HTTPException(status_code=400, detail="text too long")

    return get_agent_response(text)
