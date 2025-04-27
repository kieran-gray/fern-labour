from fastapi.testclient import TestClient


async def test_can_redirect_to_docs_from_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.history[0].status_code == 307  # Redirected
    assert response.status_code == 200


async def test_can_access_docs(client: TestClient) -> None:
    response = client.get("/docs")
    assert response.status_code == 200


def test_can_access_openapi_spec(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_can_access_redoc(client: TestClient) -> None:
    response = client.get("/redoc")
    assert response.status_code == 200
