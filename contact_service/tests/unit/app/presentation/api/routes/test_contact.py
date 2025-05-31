from fastapi.testclient import TestClient


def test_contact_us_send_message(client: TestClient) -> None:
    """Test sending a valid contact message."""
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
    assert response.status_code == 201


def test_contact_us_send_message_invalid_email(client: TestClient) -> None:
    """Test sending a contact message with invalid email."""
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "category": "error_report",
            "token": "test_token",
            "email": "@example.com",
            "name": "Test User",
            "message": "Test message",
            "user_id": "test_user_id",
        },
    )
    assert response.status_code == 422


def test_contact_us_send_message_missing_data(client: TestClient) -> None:
    """Test sending a contact message with missing required fields."""
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "token": "test_token",
            "email": "test@example.com",
        },
    )
    assert response.status_code == 422


def test_contact_us_email_too_long(client: TestClient) -> None:
    """Test sending a contact message with email exceeding max length."""
    long_email = "a" * 250 + "@example.com"  # Exceeds EMAIL_MAX_LENGTH of 254
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "category": "error_report",
            "token": "test_token",
            "email": long_email,
            "name": "Test User",
            "message": "Test message",
        },
    )
    assert response.status_code == 422


def test_contact_us_invalid_email_format(client: TestClient) -> None:
    """Test sending a contact message with invalid email format."""
    invalid_emails = [
        "invalid-email",
        "test@",
        "@example.com",
        "test!test@example.com",
        "test@example",
        "",
    ]

    for email in invalid_emails:
        response = client.post(
            "/api/v1/contact-us/",
            json={
                "category": "error_report",
                "token": "test_token",
                "email": email,
                "name": "Test User",
                "message": "Test message",
            },
        )
        assert response.status_code == 422


def test_contact_us_name_too_long(client: TestClient) -> None:
    """Test sending a contact message with name exceeding max length."""
    long_name = "a" * 101  # Exceeds NAME_MAX_LENGTH of 100
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "category": "error_report",
            "token": "test_token",
            "email": "test@example.com",
            "name": long_name,
            "message": "Test message",
        },
    )
    assert response.status_code == 422


def test_contact_us_message_too_long(client: TestClient) -> None:
    """Test sending a contact message with message exceeding max length."""
    long_message = "a" * 5001  # Exceeds MESSAGE_MAX_LENGTH of 5000
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "category": "error_report",
            "token": "test_token",
            "email": "test@example.com",
            "name": "Test User",
            "message": long_message,
        },
    )
    assert response.status_code == 422


def test_contact_us_empty_required_fields(client: TestClient) -> None:
    """Test sending a contact message with empty required fields."""
    required_fields = ["category", "email", "name", "message", "token"]

    base_data = {
        "category": "error_report",
        "token": "test_token",
        "email": "test@example.com",
        "name": "Test User",
        "message": "Test message",
    }

    for test_case in required_fields:
        test_data = base_data.copy()
        test_data[test_case] = None

        response = client.post("/api/v1/contact-us/", json=test_data)
        assert response.status_code == 422


def test_contact_us_with_optional_data(client: TestClient) -> None:
    """Test sending a contact message with optional data field."""
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "category": "error_report",
            "token": "test_token",
            "email": "test@example.com",
            "name": "Test User",
            "message": "Test message",
            "data": {"additional_info": "Some extra data"},
        },
    )
    assert response.status_code == 201


def test_contact_us_without_optional_fields(client: TestClient) -> None:
    """Test sending a contact message without optional fields (user_id, data)."""
    response = client.post(
        "/api/v1/contact-us/",
        json={
            "category": "error_report",
            "token": "test_token",
            "email": "test@example.com",
            "name": "Test User",
            "message": "Test message",
        },
    )
    assert response.status_code == 201


def test_contact_us_valid_email_formats(client: TestClient) -> None:
    """Test sending contact messages with various valid email formats."""
    valid_emails = [
        "test@example.com",
        "test.user@example.com",
        "test+tag@example.com",
        "test_user@example.co.uk",
        "123test@example.org",
        "test-user@sub.example.com",
    ]

    for email in valid_emails:
        response = client.post(
            "/api/v1/contact-us/",
            json={
                "category": "error_report",
                "token": "test_token",
                "email": email,
                "name": "Test User",
                "message": "Test message",
            },
        )
        assert response.status_code == 201


def test_contact_us_edge_case_lengths(client: TestClient) -> None:
    """Test sending contact messages with edge case lengths (at max limits)."""
    # Test email at max length (254 characters)
    max_email = "a" * 240 + "@example.com"  # Exactly 254 chars

    # Test name at max length (100 characters)
    max_name = "a" * 100

    # Test message at max length (5000 characters)
    max_message = "a" * 5000

    response = client.post(
        "/api/v1/contact-us/",
        json={
            "category": "error_report",
            "token": "test_token",
            "email": max_email,
            "name": max_name,
            "message": max_message,
        },
    )
    assert response.status_code == 201
