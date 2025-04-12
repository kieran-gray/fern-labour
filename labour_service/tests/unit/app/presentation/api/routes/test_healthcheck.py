from fastapi.testclient import TestClient


def test_healthcheck(client: TestClient) -> None:
    """Test the healthcheck endpoint returns OK status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
