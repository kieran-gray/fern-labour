from fastapi.testclient import TestClient

from app.application.dtos.subscription import SubscriptionDTO
from app.application.dtos.user import UserSummaryDTO
from app.labour.application.dtos.labour import LabourDTO


def test_subscribe_to(client: TestClient, mock_subscription_dto: SubscriptionDTO) -> None:
    """Test subscribing to a labour."""
    response = client.post(
        f"/api/v1/subscription/subscribe/{mock_subscription_dto.labour_id}",
        headers={"Authorization": "Bearer test_token"},
        json={"token": "test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {"subscription": mock_subscription_dto.to_dict()}


def test_unsubscribe_from(client: TestClient, mock_subscription_dto: SubscriptionDTO) -> None:
    """Test unsubscribing from a labour."""
    response = client.post(
        "/api/v1/subscription/unsubscribe",
        headers={"Authorization": "Bearer test_token"},
        json={"labour_id": mock_subscription_dto.labour_id},
    )

    unsubscribed = mock_subscription_dto.to_dict()
    unsubscribed["status"] = "unsubscribed"

    assert response.status_code == 200
    assert response.json() == {"subscription": unsubscribed}


def test_get_subscriptions(client: TestClient, mock_subscription_dto: SubscriptionDTO) -> None:
    """Test getting all subscriptions."""
    response = client.get(
        "/api/v1/subscription/subscriptions",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {"subscriptions": [mock_subscription_dto.to_dict()]}


def test_get_subscriber_subscriptions(
    client: TestClient,
    mock_subscription_dto: SubscriptionDTO,
    mock_user_summary_dto: UserSummaryDTO,
) -> None:
    """Test getting subscriber subscriptions with birthing person details."""
    response = client.get(
        "/api/v1/subscription/subscriber_subscriptions",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "subscriptions": [mock_subscription_dto.to_dict()],
        "birthing_persons": [mock_user_summary_dto.to_dict()],
    }


def test_get_subscription_by_id(
    client: TestClient,
    mock_subscription_dto: SubscriptionDTO,
    mock_user_summary_dto: UserSummaryDTO,
    mock_labour_dto: LabourDTO,
) -> None:
    """Test getting subscription data by ID."""
    response = client.get(
        f"/api/v1/subscription/subscription-data/{mock_subscription_dto.id}",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "subscription": mock_subscription_dto.to_dict(),
        "birthing_person": mock_user_summary_dto.to_dict(),
        "labour": mock_labour_dto.to_dict(),
    }


def test_get_labour_subscriptions(
    client: TestClient,
    mock_subscription_dto: SubscriptionDTO,
    mock_user_summary_dto: UserSummaryDTO,
) -> None:
    """Test getting labour subscriptions with subscriber details."""
    response = client.get(
        f"/api/v1/subscription/labour_subscriptions/{mock_subscription_dto.labour_id}",
        headers={"Authorization": "Bearer test_token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "subscriptions": [mock_subscription_dto.to_dict()],
        "subscribers": [mock_user_summary_dto.to_dict()],
    }


def test_subscribe_to_unauthorized(client: TestClient) -> None:
    """Test subscribing to a labour without authorization."""
    response = client.post("/api/v1/subscription/subscribe/test_id")
    assert response.status_code == 403


def test_unsubscribe_from_unauthorized(client: TestClient) -> None:
    """Test unsubscribing from a labour without authorization."""
    response = client.post("/api/v1/subscription/unsubscribe")
    assert response.status_code == 403


def test_get_subscriptions_unauthorized(client: TestClient) -> None:
    """Test getting subscriptions without authorization."""
    response = client.get("/api/v1/subscription/subscriptions")
    assert response.status_code == 403


def test_subscribe_to_invalid_token(
    client: TestClient, mock_subscription_dto: SubscriptionDTO
) -> None:
    """Test subscribing to a labour with invalid token."""
    response = client.post(
        f"/api/v1/subscription/subscribe/{mock_subscription_dto.labour_id}",
        headers={"Authorization": "Bearer invalid_token"},
        json={"token": "test_token"},
    )
    assert response.status_code == 401


def test_unsubscribe_from_invalid_token(
    client: TestClient, mock_subscription_dto: SubscriptionDTO
) -> None:
    """Test unsubscribing from a labour with invalid token."""
    response = client.post(
        "/api/v1/subscription/unsubscribe",
        headers={"Authorization": "Bearer invalid_token"},
        json={"labour_id": mock_subscription_dto.labour_id},
    )
    assert response.status_code == 401


def test_get_subscriptions_invalid_token(client: TestClient) -> None:
    """Test getting subscriptions with invalid token."""
    response = client.get(
        "/api/v1/subscription/subscriptions",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
