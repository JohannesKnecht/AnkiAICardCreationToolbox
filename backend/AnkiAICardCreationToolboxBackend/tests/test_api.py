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
    response.json()  # test json deocing
    assert "http" in response.text.lower()


def test_rate_limit_blocks_second_request_from_same_ip():
    """Verify a second request from the same IP within the window gets blocked."""
    first = client.post("/create_cards", json={"text": "first request"})
    assert first.status_code == 200

    second = client.post("/create_cards", json={"text": "second request"})
    assert second.status_code == 429


def test_rate_limit_is_applied_per_ip():
    """Verify different client IPs have independent rate limits."""
    first_ip = {"x-forwarded-for": "1.2.3.4"}
    second_ip = {"x-forwarded-for": "5.6.7.8"}

    first = client.post("/create_cards", json={"text": "first ip request"}, headers=first_ip)
    second = client.post("/create_cards", json={"text": "second ip request"}, headers=second_ip)

    assert first.status_code == 200
    assert second.status_code == 200
