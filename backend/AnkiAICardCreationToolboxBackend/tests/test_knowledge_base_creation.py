"""Tests for knowledge base creation workflows."""

import tempfile

from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend import (
    invoke_anki_formatting_guidelines,
    invoke_best_practices_of_formulating_knowledge,
)
from ankiaicardcreationtoolboxbackend.main import app

client = TestClient(app)


def test_create_knowledge_base():
    """Verify that both knowledge bases can be created in a temp directory."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        invoke_best_practices_of_formulating_knowledge(tmpdirname)
        invoke_anki_formatting_guidelines(tmpdirname)
