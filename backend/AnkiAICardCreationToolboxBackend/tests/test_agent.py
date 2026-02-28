"""Tests for agent tool functions."""

from ankiaicardcreationtoolboxbackend.tools import anki_formatting_guidelines, best_practices_of_formulating_knowledge


def test_tools():
    """Verify that knowledge base tool functions return data successfully."""
    best_practices_of_formulating_knowledge()
    anki_formatting_guidelines()
