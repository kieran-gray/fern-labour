from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.application.dtos.labour import LabourDTO


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


def test_begin_labour(client: TestClient, mock_labour_dto: LabourDTO) -> None:
    """Test beginning a labour."""
    response = client.post(
        "/api/v1/labour/begin",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {"labour": mock_labour_dto.to_dict()}


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
