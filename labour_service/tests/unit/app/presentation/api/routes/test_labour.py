from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from src.labour.application.dtos.labour import LabourDTO


def test_get_all_labours(client: TestClient, mock_labour_dto: LabourDTO) -> None:
    """Test getting all labours."""
    response = client.get(
        "/api/v1/labour/get-all",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {"labours": [mock_labour_dto.to_dict()]}


def test_get_labour_by_id(
    client: TestClient,
    mock_labour_dto: LabourDTO,
) -> None:
    """Test getting a labour by ID."""
    response = client.get(
        f"/api/v1/labour/get/{mock_labour_dto.id}",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {"labour": mock_labour_dto.to_dict()}


def test_plan_labour(client: TestClient, mock_labour_dto: LabourDTO) -> None:
    """Test planning a new labour."""
    response = client.post(
        "/api/v1/labour/plan",
        headers={"Authorization": "Bearer test_token"},
        json={
            "first_labour": True,
            "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "labour_name": "Test Labour",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"labour": mock_labour_dto.to_dict()}


def test_plan_labour_name_at_max_length(client: TestClient) -> None:
    """Test planning labour with labour_name at max length (255 characters)."""
    max_length_name = "a" * 255  # Exactly 255 characters
    response = client.post(
        "/api/v1/labour/plan",
        headers={"Authorization": "Bearer test_token"},
        json={
            "first_labour": True,
            "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "labour_name": max_length_name,
        },
    )
    assert response.status_code == 200


def test_plan_labour_name_exceeds_max_length(client: TestClient) -> None:
    """Test planning labour with labour_name exceeding max length (255 characters)."""
    too_long_name = "a" * 256  # Exceeds 255 character limit
    response = client.post(
        "/api/v1/labour/plan",
        headers={"Authorization": "Bearer test_token"},
        json={
            "first_labour": True,
            "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "labour_name": too_long_name,
        },
    )
    assert response.status_code == 422


def test_plan_labour_name_much_longer_than_max(client: TestClient) -> None:
    """Test planning labour with labour_name much longer than max length."""
    very_long_name = "a" * 1000  # Way over the 255 character limit
    response = client.post(
        "/api/v1/labour/plan",
        headers={"Authorization": "Bearer test_token"},
        json={
            "first_labour": True,
            "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "labour_name": very_long_name,
        },
    )
    assert response.status_code == 422


def test_plan_labour_name_one_character(client: TestClient) -> None:
    """Test planning labour with labour_name of one character."""
    response = client.post(
        "/api/v1/labour/plan",
        headers={"Authorization": "Bearer test_token"},
        json={
            "first_labour": True,
            "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "labour_name": "A",
        },
    )
    assert response.status_code == 200


def test_begin_labour(client: TestClient, mock_labour_dto: LabourDTO) -> None:
    """Test beginning a labour."""
    response = client.post(
        "/api/v1/labour/begin",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {"labour": mock_labour_dto.to_dict()}


def test_complete_labour_with_both_fields(client: TestClient) -> None:
    """Test completing labour with both end_time and notes."""
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": datetime.now().isoformat(),
            "notes": "Labour went smoothly, baby arrived healthy",
        },
    )
    assert response.status_code == 200


def test_complete_labour_with_end_time_only(client: TestClient) -> None:
    """Test completing labour with only end_time."""
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": datetime.now().isoformat(),
        },
    )
    assert response.status_code == 200


def test_complete_labour_with_notes_only(client: TestClient) -> None:
    """Test completing labour with only notes."""
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "notes": "Additional notes about the labour experience",
        },
    )
    assert response.status_code == 200


def test_complete_labour_with_no_fields(client: TestClient) -> None:
    """Test completing labour with no fields (both optional)."""
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={},
    )
    assert response.status_code == 200


def test_complete_labour_notes_at_max_length(client: TestClient) -> None:
    """Test completing labour with notes at max length (1000 characters)."""
    max_length_notes = "a" * 1000  # Exactly 1000 characters
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": datetime.now().isoformat(),
            "notes": max_length_notes,
        },
    )
    assert response.status_code == 200


def test_complete_labour_notes_exceeds_max_length(client: TestClient) -> None:
    """Test completing labour with notes exceeding max length (1000 characters)."""
    too_long_notes = "a" * 1001  # Exceeds 1000 character limit
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": datetime.now().isoformat(),
            "notes": too_long_notes,
        },
    )
    assert response.status_code == 422


def test_complete_labour_notes_much_longer_than_max(client: TestClient) -> None:
    """Test completing labour with notes much longer than max length."""
    very_long_notes = "a" * 2000  # Way over the 1000 character limit
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": datetime.now().isoformat(),
            "notes": very_long_notes,
        },
    )
    assert response.status_code == 422


def test_complete_labour_notes_empty_string(client: TestClient) -> None:
    """Test completing labour with empty notes string."""
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": datetime.now().isoformat(),
            "notes": "",
        },
    )
    assert response.status_code == 200


def test_complete_labour_notes_one_character(client: TestClient) -> None:
    """Test completing labour with notes of one character."""
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": datetime.now().isoformat(),
            "notes": "A",
        },
    )
    assert response.status_code == 200


def test_complete_labour_notes_null(client: TestClient) -> None:
    """Test completing labour with null notes."""
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": datetime.now().isoformat(),
            "notes": None,
        },
    )
    assert response.status_code == 200


def test_complete_labour_end_time_null(client: TestClient) -> None:
    """Test completing labour with null end_time."""
    response = client.put(
        "/api/v1/labour/complete",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": None,
            "notes": "Some completion notes",
        },
    )
    assert response.status_code == 200


def test_start_contraction(client: TestClient, mock_labour_dto: LabourDTO) -> None:
    """Test starting a contraction."""
    start_time = datetime.now()
    response = client.post(
        "/api/v1/labour/contraction/start",
        headers={"Authorization": "Bearer test_token"},
        json={
            "start_time": start_time.isoformat(),
            "intensity": 5,
            "notes": "Test contraction",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"labour": mock_labour_dto.to_dict()}


def test_end_contraction(client: TestClient, mock_labour_dto: LabourDTO) -> None:
    """Test ending a contraction."""
    end_time = datetime.now()
    response = client.put(
        "/api/v1/labour/contraction/end",
        headers={"Authorization": "Bearer test_token"},
        json={
            "end_time": end_time.isoformat(),
            "intensity": 5,
            "notes": "Test contraction ended",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"labour": mock_labour_dto.to_dict()}


def test_get_all_labours_unauthorized(client: TestClient) -> None:
    """Test getting all labours without authorization."""
    response = client.get("/api/v1/labour/get-all")
    assert response.status_code == 403


def test_get_labour_by_id_unauthorized(client: TestClient) -> None:
    """Test getting a labour by ID without authorization."""
    response = client.get("/api/v1/labour/get/test_id")
    assert response.status_code == 403


def test_plan_labour_unauthorized(client: TestClient) -> None:
    """Test planning a labour without authorization."""
    response = client.post("/api/v1/labour/plan")
    assert response.status_code == 403


def test_get_all_labours_invalid_token(client: TestClient) -> None:
    """Test getting all labours with invalid token."""
    response = client.get(
        "/api/v1/labour/get-all",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401


def test_get_labour_by_id_invalid_token(client: TestClient) -> None:
    """Test getting a labour by ID with invalid token."""
    response = client.get(
        "/api/v1/labour/get/test_id",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401


def test_labour_update_create_valid_announcement(client: TestClient) -> None:
    """Test creating a valid labour update with announcement type."""
    response = client.post(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_type": "announcement",
            "message": "Baby is on the way! Labour has started.",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_labour_update_create_valid_status_update(client: TestClient) -> None:
    """Test creating a valid labour update with status_update type."""
    response = client.post(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_type": "status_update",
            "message": "Contractions are 5 minutes apart and getting stronger.",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_labour_update_create_valid_private_note(client: TestClient) -> None:
    """Test creating a valid labour update with private_note type."""
    response = client.post(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_type": "private_note",
            "message": "Personal notes for medical team only.",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_labour_update_create_with_sent_time(client: TestClient) -> None:
    """Test creating a labour update with sent_time."""
    response = client.post(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_type": "announcement",
            "message": "Labour has started!",
            "sent_time": "2024-01-15T10:30:00",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_labour_update_create_missing_required_fields(client: TestClient) -> None:
    """Test creating a labour update with missing required fields."""
    missing_field_tests = [
        {"message": "Test message"},  # Missing labour_update_type
        {"labour_update_type": "announcement"},  # Missing message
        {},  # Missing both required fields
    ]

    for test_data in missing_field_tests:
        response = client.post(
            "/api/v1/labour/labour-update",
            json=test_data,
            headers={"Authorization": "Bearer test_token"},
        )
        assert response.status_code == 422


def test_labour_update_create_invalid_type(client: TestClient) -> None:
    """Test creating a labour update with invalid labour_update_type."""
    invalid_types = [
        "invalid_type",
        "contraction",
        "pain_level",
        "ANNOUNCEMENT",  # Case sensitive
        "STATUS_UPDATE",  # Case sensitive
        "",
        None,
    ]

    for invalid_type in invalid_types:
        response = client.post(
            "/api/v1/labour/labour-update",
            json={
                "labour_update_type": invalid_type,
                "message": "Test message",
            },
            headers={"Authorization": "Bearer test_token"},
        )
        assert response.status_code == 422


def test_labour_update_create_message_too_long(client: TestClient) -> None:
    """Test creating a labour update with message exceeding max length."""
    long_message = "a" * 1001  # Exceeds LABOUR_UPDATE_MAX_LENGTH of 1000
    response = client.post(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_type": "announcement",
            "message": long_message,
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 422


def test_labour_update_create_message_at_max_length(client: TestClient) -> None:
    """Test creating a labour update with message at max length."""
    max_message = "a" * 1000  # Exactly LABOUR_UPDATE_MAX_LENGTH
    response = client.post(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_type": "status_update",
            "message": max_message,
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_labour_update_create_empty_message(client: TestClient) -> None:
    """Test creating a labour update with empty message."""
    response = client.post(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_type": "private_note",
            "message": None,
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 422


def test_labour_update_create_invalid_datetime(client: TestClient) -> None:
    """Test creating a labour update with invalid datetime format."""
    invalid_datetimes = [
        "invalid-datetime",
        "2024-13-01T10:30:00",  # Invalid month
        "2024-01-32T10:30:00",  # Invalid day
        "2024-01-01T25:30:00",  # Invalid hour
        "not-a-date",
        "",
    ]

    for invalid_datetime in invalid_datetimes:
        response = client.post(
            "/api/v1/labour/labour-update",
            json={
                "labour_update_type": "announcement",
                "message": "Test message",
                "sent_time": invalid_datetime,
            },
            headers={"Authorization": "Bearer test_token"},
        )
        assert response.status_code == 422


def test_labour_update_create_valid_datetime_formats(client: TestClient) -> None:
    """Test creating labour updates with various valid datetime formats."""
    valid_datetimes = [
        "2024-01-15T10:30:00",
        "2024-01-15T10:30:00.123",
        "2024-01-15T10:30:00Z",
        "2024-01-15T10:30:00+00:00",
        "2024-01-15T10:30:00-05:00",
    ]

    for valid_datetime in valid_datetimes:
        response = client.post(
            "/api/v1/labour/labour-update",
            json={
                "labour_update_type": "announcement",
                "message": "Test message",
                "sent_time": valid_datetime,
            },
            headers={"Authorization": "Bearer test_token"},
        )
        assert response.status_code == 200


def test_update_labour_update_valid_all_fields(client: TestClient) -> None:
    """Test updating a labour update with all fields."""
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_id": "update123",
            "labour_update_type": "status_update",
            "message": "Updated labour progress information",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_update_labour_update_partial_message_only(client: TestClient) -> None:
    """Test updating a labour update with only message."""
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_id": "update123",
            "message": "Updated message only",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_update_labour_update_partial_type_only(client: TestClient) -> None:
    """Test updating a labour update with only labour_update_type."""
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_id": "update123",
            "labour_update_type": "private_note",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_update_labour_update_missing_id(client: TestClient) -> None:
    """Test updating a labour update without labour_update_id."""
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_type": "announcement",
            "message": "Test message",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 422


def test_update_labour_update_message_too_long(client: TestClient) -> None:
    """Test updating a labour update with message exceeding max length."""
    long_message = "a" * 1001  # Exceeds LABOUR_UPDATE_MAX_LENGTH of 1000
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_id": "update123",
            "message": long_message,
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 422


def test_update_labour_update_message_at_max_length(client: TestClient) -> None:
    """Test updating a labour update with message at max length."""
    max_message = "a" * 1000  # Exactly LABOUR_UPDATE_MAX_LENGTH
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_id": "update123",
            "message": max_message,
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_update_labour_update_null_message(client: TestClient) -> None:
    """Test updating a labour update with null message."""
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_id": "update123",
            "message": None,
            "labour_update_type": "announcement",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_update_labour_update_invalid_type(client: TestClient) -> None:
    """Test updating a labour update with invalid labour_update_type."""
    invalid_types = [
        "invalid_type",
        "contraction",
        "ANNOUNCEMENT",  # Case sensitive
        "STATUS_UPDATE",  # Case sensitive
        "PRIVATE_NOTE",  # Case sensitive
        "",
    ]

    for invalid_type in invalid_types:
        response = client.put(
            "/api/v1/labour/labour-update",
            json={
                "labour_update_id": "update123",
                "labour_update_type": invalid_type,
                "message": "Test message",
            },
            headers={"Authorization": "Bearer test_token"},
        )
        assert response.status_code == 422


def test_update_labour_update_valid_types(client: TestClient) -> None:
    """Test updating labour update with all valid labour_update_type values."""
    valid_types = ["announcement", "status_update", "private_note"]

    for valid_type in valid_types:
        response = client.put(
            "/api/v1/labour/labour-update",
            json={
                "labour_update_id": "update123",
                "labour_update_type": valid_type,
                "message": f"Test message for {valid_type}",
            },
            headers={"Authorization": "Bearer test_token"},
        )
        assert response.status_code == 200


def test_update_labour_update_only_required_id(client: TestClient) -> None:
    """Test updating a labour update with only required labour_update_id."""
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_id": "update123",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200


def test_update_labour_update_null_type(client: TestClient) -> None:
    """Test updating a labour update with null labour_update_type."""
    response = client.put(
        "/api/v1/labour/labour-update",
        json={
            "labour_update_id": "update123",
            "labour_update_type": None,
            "message": "Test message with null type",
        },
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200
