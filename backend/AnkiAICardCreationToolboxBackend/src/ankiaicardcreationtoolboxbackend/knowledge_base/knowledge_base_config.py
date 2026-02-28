"""Configuration for knowledge base sources and paths."""

import os

PROJECT_KNOWLEDGE_DIR = "src/ankiaicardcreationtoolboxbackend/data"
if os.path.isfile("./pyproject.toml"):
    PROJECT_KNOWLEDGE_BASE_DIR = PROJECT_KNOWLEDGE_DIR
else:
    PROJECT_KNOWLEDGE_BASE_DIR = f"backend/AnkiAICardCreationToolboxBackend/{PROJECT_KNOWLEDGE_DIR}"


BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE = "BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE"
ANKI_FORMATTING_GUIDELINES = "ANKI_FORMATTING_GUIDELINES"

knowledge_base_config: dict[str, dict[str, str]] = {
    BEST_PRACTICES_OF_FORMULATING_KNOWLEDGE: {
        "url": "https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge",
        "additional_info": "",
    },
    ANKI_FORMATTING_GUIDELINES: {
        "url": "https://docs.ankiweb.net/importing/text-files.html#text-files",
        "additional_info": """
        Focus only on text files and providing a document that can be used to create such text files.
        The goal is to create text files, not to ingest them.
        """.strip(),
    },
}
