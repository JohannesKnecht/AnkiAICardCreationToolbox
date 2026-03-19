"""Tests for knowledge base creation workflows."""

import json
import socket
import tempfile
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend import (
    invoke_anki_formatting_guidelines,
    invoke_best_practices_of_formulating_knowledge,
)
from ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_creation import create_knowledge_base
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


# ---------------------------------------------------------------------------
# Diagnostic logging tests – verify instrumentation without hiding failures
# ---------------------------------------------------------------------------

_KB_LOGGER = "ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_creation"


def test_fetch_none_emits_warning_and_raises(caplog: pytest.LogCaptureFixture) -> None:
    """Warning is logged and ValueError is raised when fetch_url returns None.

    This exercises the failure path that is observed in CI when the network
    cannot reach the target URL.  We patch at the call site rather than in a
    global conftest fixture so the real trafilatura is used for all other tests.
    """
    with (
        tempfile.TemporaryDirectory() as tmpdir,
        patch("trafilatura.fetch_url", return_value=None) as mock_fetch,
        patch("trafilatura.extract", return_value=None) as mock_extract,
        pytest.raises(ValueError, match="fetch_url"),
        caplog.at_level("WARNING", logger=_KB_LOGGER),
    ):
        create_knowledge_base("https://example.invalid/page", "test_kb", "", knowledge_base_dir=tmpdir)

    mock_fetch.assert_called_once_with("https://example.invalid/page")
    mock_extract.assert_called_once_with(None)

    # fetch returned None → warning logged with structured url field
    fetch_warnings = [r for r in caplog.records if "fetch_url returned None" in r.message]
    assert fetch_warnings, "Expected a warning log entry for fetch_url returning None"
    assert getattr(fetch_warnings[0], "url", None) == "https://example.invalid/page"

    # extract returned None → warning logged
    extract_warnings = [r for r in caplog.records if "extract returned None" in r.message]
    assert extract_warnings, "Expected a warning log entry for extract returning None"

    # error-level abort entry present
    abort_errors = [r for r in caplog.records if "aborted" in r.message]
    assert abort_errors, "Expected an error log entry for aborted creation"


def test_fetch_none_raw_json_written() -> None:
    """Raw JSON is still written to disk even when extraction fails.

    This preserves diagnostic evidence (e.g. the raw HTML bytes or None) so
    that the failure can be inspected after the run.
    """
    with tempfile.TemporaryDirectory() as tmpdir:  # noqa: SIM117
        with (
            patch("trafilatura.fetch_url", return_value=None),
            patch("trafilatura.extract", return_value=None),
            pytest.raises(ValueError),
        ):
            create_knowledge_base("https://example.invalid/page", "diag_kb", "", knowledge_base_dir=tmpdir)

        with open(f"{tmpdir}/diag_kb_raw.json") as f:
            raw = json.load(f)
    assert raw == {"data": None}, f"Expected raw JSON with null data, got {raw!r}"


def test_fetch_exception_logged_and_reraised(caplog: pytest.LogCaptureFixture) -> None:
    """Connection-level exceptions from fetch_url are logged and re-raised.

    The log entry must contain the traceback text so that CI logs capture the
    full exception chain without any information being swallowed.
    """

    class _FetchError(OSError):
        pass

    with (
        tempfile.TemporaryDirectory() as tmpdir,
        patch("trafilatura.fetch_url", side_effect=_FetchError("connection refused")),
        pytest.raises(_FetchError, match="connection refused"),
        caplog.at_level("ERROR", logger=_KB_LOGGER),
    ):
        create_knowledge_base("https://example.invalid/page", "exc_kb", "", knowledge_base_dir=tmpdir)

    error_records = [r for r in caplog.records if "fetch_url raised an unexpected exception" in r.message]
    assert error_records, "Expected an error log entry when fetch_url raises"
    tb = getattr(error_records[0], "traceback", "")
    assert "connection refused" in tb, f"Expected traceback to contain exception message, got: {tb!r}"


def test_successful_fetch_logs_bytes_and_chars(caplog: pytest.LogCaptureFixture) -> None:
    """Successful fetch and extraction log byte count and character count.

    These structured fields let us diagnose whether content was retrieved but
    was too short/malformed for the LLM summarisation step.
    """
    fake_html = "<html><body><p>Hello world, this is test content.</p></body></html>"
    fake_text = "Hello world, this is test content."
    fake_summary = "Summary."

    with (
        tempfile.TemporaryDirectory() as tmpdir,
        patch("trafilatura.fetch_url", return_value=fake_html),
        patch("trafilatura.extract", return_value=fake_text),
        patch("ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_creation.get_model") as mock_model,
        caplog.at_level("INFO", logger=_KB_LOGGER),
    ):
        mock_model.return_value.invoke.return_value.content = fake_summary
        create_knowledge_base("https://example.com/page", "ok_kb", "", knowledge_base_dir=tmpdir)

    fetch_info = [r for r in caplog.records if "fetch_url completed" in r.message]
    assert fetch_info, "Expected an info log entry for successful fetch"
    assert getattr(fetch_info[0], "downloaded_bytes", None) == len(fake_html)

    extract_info = [r for r in caplog.records if "extract completed" in r.message]
    assert extract_info, "Expected an info log entry for successful extraction"
    assert getattr(extract_info[0], "extracted_chars", None) == len(fake_text)

    success_info = [r for r in caplog.records if "knowledge-base creation succeeded" in r.message]
    assert success_info, "Expected a success log entry at the end of creation"


def test_error_message_includes_url_and_request_id() -> None:
    """ValueError message contains the URL and a request_id for correlation."""
    with (
        tempfile.TemporaryDirectory() as tmpdir,
        patch("trafilatura.fetch_url", return_value=None),
        patch("trafilatura.extract", return_value=None),
        pytest.raises(ValueError) as exc_info,
    ):
        create_knowledge_base("https://example.invalid/page", "msg_kb", "", knowledge_base_dir=tmpdir)

    msg = str(exc_info.value)
    assert "https://example.invalid/page" in msg, f"URL missing from error message: {msg!r}"
    assert "request_id=" in msg, f"request_id missing from error message: {msg!r}"
