from fastapi.testclient import TestClient


def test_login_success(client: TestClient) -> None:
    """Test successful login returns token."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test_user", "password": "test_password"},
    )

    assert response.status_code == 200
    assert response.json() == {"access_token": "test_token", "token_type": "Bearer"}


def test_login_invalid_credentials(client: TestClient) -> None:
    """Test login with invalid credentials returns error."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong_user", "password": "wrong_password"},
    )

    assert response.status_code == 401
