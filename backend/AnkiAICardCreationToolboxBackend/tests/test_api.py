"""Tests for the FastAPI card creation endpoint."""

import pytest
from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend.main import app, clear_rate_limit_state

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_rate_limit_between_tests():
    """Reset in-memory rate limiting so tests are independent."""
    clear_rate_limit_state()


def test_read_main():
    """Verify that the create_cards endpoint returns a successful JSON response."""
    response = client.post("/create_cards", json={"text": "Anki Karten zur Funktionsweise von HTTP"})
    assert response.status_code == 200
    response.json()  # test json decoding
    assert "http" in response.text.lower()


def test_rate_limit_blocks_second_request_from_same_ip():
    """Verify a second request within the window gets blocked."""
    first = client.post("/create_cards", json={"text": "first request"})
    assert first.status_code == 200

    second = client.post("/create_cards", json={"text": "second request"})
    assert second.status_code == 429
    retry_after = second.headers.get("retry-after")
    assert retry_after is not None
    assert retry_after.isdigit()
    assert 590 <= int(retry_after) <= 600


def test_rate_limit_is_global_across_ips(monkeypatch):
    """Verify different client IPs still share the same global rate limit."""
    monkeypatch.setenv("TRUST_X_FORWARDED_FOR", "1")
    first_ip = {"x-forwarded-for": "1.2.3.4"}
    second_ip = {"x-forwarded-for": "5.6.7.8"}

    first = client.post("/create_cards", json={"text": "first ip request"}, headers=first_ip)
    second = client.post("/create_cards", json={"text": "second ip request"}, headers=second_ip)

    assert first.status_code == 200
    assert second.status_code == 429
