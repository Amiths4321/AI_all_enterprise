from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_ready():

    response = client.get("/ready")

    assert response.status_code == 200

    assert response.json()["status"] == "ready"


def test_query_validation():

    response = client.post(
        "/query",
        json={
            "question": "",
        },
    )

    assert response.status_code == 422