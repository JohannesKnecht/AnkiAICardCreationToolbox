"""Tests for knowledge base creation workflows."""

import socket
import tempfile

import pytest
from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend import (
    invoke_anki_formatting_guidelines,
    invoke_best_practices_of_formulating_knowledge,
)
from ankiaicardcreationtoolboxbackend.main import app

client = TestClient(app)


def _network_available() -> bool:
    """Return True when outbound DNS resolution is reachable.

    Uses the same hostname as the first knowledge-base source so the skip
    condition mirrors the real failure condition.
    """
    try:
        socket.getaddrinfo("www.supermemo.com", 443, type=socket.SOCK_STREAM)
        return True
    except OSError:
        return False


@pytest.mark.skipif(not _network_available(), reason="Requires outbound network access")
def test_create_knowledge_base():
    """Verify that both knowledge bases can be created in a temp directory."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        invoke_best_practices_of_formulating_knowledge(tmpdirname)
        invoke_anki_formatting_guidelines(tmpdirname)
