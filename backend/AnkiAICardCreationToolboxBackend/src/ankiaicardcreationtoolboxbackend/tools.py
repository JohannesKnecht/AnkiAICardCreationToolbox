import json

from ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_config import \
    BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE, ANKI_FORMATTING_GUIDELINES, PROJECT_KNOWLEDGE_BASE_DIR


def get_data(file: str) -> dict[str, str]:
    with open(f"{PROJECT_KNOWLEDGE_BASE_DIR}/{file}.json", 'r') as f:
        return json.load(f)


def best_practices_of_formulating_knowledge() -> str:
    """Get best practices of formulating knowledge"""
    return get_data(BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE)


def anki_formatting_guidelines() -> str:
    """Get best practices of formulating knowledge"""
    return get_data(ANKI_FORMATTING_GUIDELINES)
