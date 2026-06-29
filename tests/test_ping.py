from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


def test_wrong_path():
    response = client.get("/pingg")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

