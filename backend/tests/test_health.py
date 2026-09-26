from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "health" in data


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "LITERA API"
    assert "timestamp" in data
    assert "version" in data
    assert "environment" in data


def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "html" in response.headers.get("content-type", "")


def test_openapi_json_endpoint():
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert data["info"]["title"] == "LITERA API"

