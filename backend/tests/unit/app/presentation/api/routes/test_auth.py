from fastapi.testclient import TestClient

from app.user.application.dtos.user import UserDTO


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


def test_get_user_success(client: TestClient, test_user: UserDTO) -> None:
    """Test getting authenticated user information."""
    response = client.get(
        "/api/v1/auth/user",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": test_user.id,
        "username": test_user.username,
        "email": test_user.email,
        "first_name": test_user.first_name,
        "last_name": test_user.last_name,
        "phone_number": test_user.phone_number,
    }


def test_get_user_invalid_token(client: TestClient) -> None:
    """Test getting user information with invalid token returns error."""
    response = client.get(
        "/api/v1/auth/user",
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401


def test_get_user_missing_token(client: TestClient) -> None:
    """Test getting user information without token returns error."""
    response = client.get("/api/v1/auth/user")
    assert response.status_code == 403
