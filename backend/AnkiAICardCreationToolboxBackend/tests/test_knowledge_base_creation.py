from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend import create_knowledge_base
from ankiaicardcreationtoolboxbackend.main import (app)

client = TestClient(app)


def test_create_knowledge_base():
    create_knowledge_base()

