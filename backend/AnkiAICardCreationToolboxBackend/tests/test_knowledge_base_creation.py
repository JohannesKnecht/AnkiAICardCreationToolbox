from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend import create_knowledge_base, invoke_best_practices_of_formulating_knowledge, \
    invoke_anki_formatting_guidelines
from ankiaicardcreationtoolboxbackend.main import (app)
import tempfile

client = TestClient(app)


def test_create_knowledge_base():
    with tempfile.TemporaryDirectory() as tmpdirname:
        invoke_best_practices_of_formulating_knowledge(tmpdirname)
        invoke_anki_formatting_guidelines(tmpdirname)
