from fastapi.testclient import TestClient

from src.user.application.dtos.user import UserDTO


def test_get_user(client: TestClient, test_user: UserDTO) -> None:
    """Test getting user information."""
    response = client.get(
        "/api/v1/user/",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user": {
            "id": test_user.id,
            "username": test_user.username,
            "email": test_user.email,
            "first_name": test_user.first_name,
            "last_name": test_user.last_name,
            "phone_number": test_user.phone_number,
        }
    }


def test_get_user_summary(client: TestClient, test_user: UserDTO) -> None:
    """Test getting user summary information."""
    response = client.get(
        "/api/v1/user/summary",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user": {
            "id": test_user.id,
            "first_name": test_user.first_name,
            "last_name": test_user.last_name,
        }
    }


def test_get_user_unauthorized(client: TestClient) -> None:
    """Test getting user information without authorization."""
    response = client.get("/api/v1/user/")
    assert response.status_code == 403


def test_get_user_summary_unauthorized(client: TestClient) -> None:
    """Test getting user summary without authorization."""
    response = client.get("/api/v1/user/summary")
    assert response.status_code == 403


def test_get_user_invalid_token(client: TestClient) -> None:
    """Test getting user information with invalid token."""
    response = client.get(
        "/api/v1/user/",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401


def test_get_user_summary_invalid_token(client: TestClient) -> None:
    """Test getting user summary with invalid token."""
    response = client.get(
        "/api/v1/user/summary",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
