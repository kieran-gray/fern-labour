from fastapi.testclient import TestClient


def test_contact_us_send_message(
    client: TestClient,
) -> None:
    """Test sending a contact message."""
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "category": "error_report",
            "token": "test_token",
            "email": "test@example.com",
            "name": "Test User",
            "message": "Test message",
            "user_id": "test_user_id",
        },
    )

    assert response.status_code == 204


def test_contact_us_send_message_missing_data(client: TestClient) -> None:
    """Test sending a contact message with missing data."""
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "token": "test_token",
            "email": "test@example.com",
        },
    )

    assert response.status_code == 422
