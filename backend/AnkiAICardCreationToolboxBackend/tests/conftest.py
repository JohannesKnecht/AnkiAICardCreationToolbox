"""Shared test configuration and fixtures."""

import os
from unittest.mock import MagicMock, patch

from dotenv import load_dotenv

load_dotenv()

# Detect mock mode.  The master pytest process sees no key and sets
# _MOCK_OPENAI=1 + a dummy key.  pytest-xdist workers inherit both
# env-vars, so they can detect mock mode reliably via the flag.
MOCK_LLM = os.environ.get("_MOCK_OPENAI") == "1" or not os.environ.get("OPENAI_API_KEY")

if MOCK_LLM:
    os.environ["_MOCK_OPENAI"] = "1"
    os.environ["OPENAI_API_KEY"] = "mock-key-for-testing"

    from langchain_core.messages import AIMessage
    from langchain_core.outputs import ChatGeneration, ChatResult

    def _mock_generate(self, messages, stop=None, run_manager=None, **kwargs):
        """Return a fake ChatResult for all OpenAI model calls."""
        # Responses API (used by deepagents) returns content as a list of blocks;
        # Chat Completions API returns content as a plain string.
        content: str | list[str | dict]
        if getattr(self, "use_responses_api", False):
            content = [{"type": "text", "text": "Mocked http response content"}]
        else:
            content = "Mocked http response content"
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    # Patch the OpenAI chat model at the langchain level so that *every* LLM call
    # (from deepagents, knowledge-base creation, etc.) is intercepted regardless of
    # how the caller obtained the model instance.  Applied at module scope so the
    # patch is active before any test code runs – including inside pytest-xdist workers.
    patch("langchain_openai.chat_models.base.BaseChatOpenAI._generate", _mock_generate).start()

    # Patch outbound HTTP requests used by _fetch_html so tests never contact
    # external sites (e.g. supermemo.com blocks automated requests).
    _mock_http_response = MagicMock()
    _mock_http_response.text = "<html><body><p>Mock page content for testing.</p></body></html>"
    _mock_http_response.raise_for_status = lambda: None
    patch(
        "ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_creation.requests.get",
        return_value=_mock_http_response,
    ).start()

    # Patch trafilatura.extract so it returns predictable text without
    # processing the mocked HTML through the real extraction pipeline.
    patch(
        "ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_creation.trafilatura.extract",
        return_value="Mock extracted text content for testing.",
    ).start()

else:
    # Use the cheapest model for real API tests unless explicitly overridden
    if not os.environ.get("OPENAI_MODEL_OVERRIDE"):
        os.environ["OPENAI_MODEL_OVERRIDE"] = "gpt-4.1-nano"
