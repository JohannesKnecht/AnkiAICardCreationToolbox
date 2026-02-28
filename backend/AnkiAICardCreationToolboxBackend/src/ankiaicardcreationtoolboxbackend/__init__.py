"""Anki AI Card Creation Toolbox backend package."""

import asyncio

from dotenv import load_dotenv

from ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_config import (
    ANKI_FORMATTING_GUIDELINES,
    BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE,
)
from ankiaicardcreationtoolboxbackend.knowledge_base.knowledge_base_creation import (
    create_knowledge_base_with_config_name,
)
from ankiaicardcreationtoolboxbackend.main import CardRequestData, create_cards

load_dotenv()


def main() -> None:
    """Run the default card creation for HTTP Basics."""
    asyncio.run(create_cards(CardRequestData(text="HTTP Basics")))


def invoke_best_practices_of_formulating_knowledge(knowledge_base_dir: str | None = None) -> None:
    """Create the best practices of formulating knowledge base."""
    create_knowledge_base_with_config_name(BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE, knowledge_base_dir)


def invoke_anki_formatting_guidelines(knowledge_base_dir: str | None = None) -> None:
    """Create the Anki formatting guidelines knowledge base."""
    create_knowledge_base_with_config_name(ANKI_FORMATTING_GUIDELINES, knowledge_base_dir)


def invoke_knowledge_base_creation(knowledge_base_dir: str | None = None) -> None:
    """Create all knowledge bases."""
    invoke_best_practices_of_formulating_knowledge(knowledge_base_dir)
    invoke_anki_formatting_guidelines(knowledge_base_dir)
