from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend.main import app

client = TestClient(app)


def test_read_main():
    response = client.post("/create_cards", json={"text": "Anki Karten zur Funktionsweise von HTTP"})
    assert response.status_code == 200
    response.json()  # test json deocing
    assert "http" in response.text.lower()
