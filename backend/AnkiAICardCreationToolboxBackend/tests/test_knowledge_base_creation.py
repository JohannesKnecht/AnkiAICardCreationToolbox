import tempfile

from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend import (
    invoke_anki_formatting_guidelines,
    invoke_best_practices_of_formulating_knowledge,
)
from ankiaicardcreationtoolboxbackend.main import app

client = TestClient(app)


def test_create_knowledge_base():
    with tempfile.TemporaryDirectory() as tmpdirname:
        invoke_best_practices_of_formulating_knowledge(tmpdirname)
        invoke_anki_formatting_guidelines(tmpdirname)
