from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend.main import (app, CardRequestData)
from ankiaicardcreationtoolboxbackend.tools import best_practices_of_formulating_knowledge, anki_formatting_guidelines


def test_tools():
    best_practices_of_formulating_knowledge()
    anki_formatting_guidelines()