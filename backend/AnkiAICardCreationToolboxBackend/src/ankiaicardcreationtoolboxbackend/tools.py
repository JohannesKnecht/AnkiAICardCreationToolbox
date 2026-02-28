"""Tools for retrieving knowledge base data."""

import json

from ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_config import (
    ANKI_FORMATTING_GUIDELINES,
    BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE,
    PROJECT_KNOWLEDGE_BASE_DIR,
)


def get_data(file: str) -> dict[str, str]:
    """Load and return JSON data from a knowledge base file."""
    with open(f"{PROJECT_KNOWLEDGE_BASE_DIR}/{file}.json") as f:
        return json.load(f)


def best_practices_of_formulating_knowledge() -> dict[str, str]:
    """Get best practices of formulating knowledge."""
    return get_data(BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE)


def anki_formatting_guidelines() -> dict[str, str]:
    """Get Anki formatting guidelines."""
    return get_data(ANKI_FORMATTING_GUIDELINES)
