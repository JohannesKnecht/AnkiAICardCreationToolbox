from ankiaicardcreationtoolboxbackend.knowledge_base_creation import create_knowledge_base
import os

from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    print("Hello from ankiaicardcreationtoolboxbackend!")


def invoke_create_knowledge_base() -> None:
    create_knowledge_base(
        "src/ankiaicardcreationtoolboxbackend/data"
    )
