"""Shared test configuration and fixtures."""

import os
from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv

load_dotenv()

MOCK_LLM = not os.environ.get("OPENAI_API_KEY")

if MOCK_LLM:
    # Set a dummy key so application-level checks (e.g. resource_check) pass.
    os.environ["OPENAI_API_KEY"] = "mock-key-for-testing"
else:
    # Use the cheapest model for real API tests unless explicitly overridden
    if not os.environ.get("OPENAI_MODEL_OVERRIDE"):
        os.environ["OPENAI_MODEL_OVERRIDE"] = "gpt-4.1-nano"


@pytest.fixture(autouse=True)
def _mock_llm_calls(monkeypatch):
    """Mock external LLM and network calls when OPENAI_API_KEY is not available."""
    if not MOCK_LLM:
        return

    import sys

    from ankiaicardcreationtoolboxbackend.knowledge_base import knowledge_base_creation

    # __init__.py defines a main() function that shadows the main submodule,
    # so we retrieve the actual module object from sys.modules.
    main_module = sys.modules["ankiaicardcreationtoolboxbackend.main"]

    # Mock the agent response used by the API endpoint
    monkeypatch.setattr(main_module, "get_agent_response", lambda text: f"Mocked Anki cards about: {text}")

    # Mock trafilatura to avoid network calls during knowledge base creation
    monkeypatch.setattr(knowledge_base_creation.trafilatura, "fetch_url", lambda url: "<html>Mocked</html>")
    monkeypatch.setattr(knowledge_base_creation.trafilatura, "extract", lambda html: "Mocked extracted text content")

    # Mock the LLM model used in knowledge base creation
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Mocked knowledge base content")
    monkeypatch.setattr(knowledge_base_creation, "get_model", lambda: mock_model)
