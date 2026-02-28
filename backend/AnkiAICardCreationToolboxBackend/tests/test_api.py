from fastapi.testclient import TestClient

from ankiaicardcreationtoolboxbackend.main import CardRequestData, app

client = TestClient(app)


def test_read_main():
    response = client.post("/create_cards", data=CardRequestData(text="Anki Karten zur Funktionsweise von HTTP").json())  # type: ignore[invalid-argument-type, deprecated]

    assert response.status_code == 200
    response.json()  # test json deocing
    assert "http" in response.text.lower()
