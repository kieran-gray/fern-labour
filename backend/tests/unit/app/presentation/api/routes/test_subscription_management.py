from fastapi.testclient import TestClient

from app.subscription.application.dtos.subscription import SubscriptionDTO


def test_remove_subscriber(client: TestClient, mock_subscription_dto: SubscriptionDTO) -> None:
    """Test removing subscriber."""
    response = client.put(
        "/api/v1/subscription-management/remove-subscriber",
        headers={"Authorization": "Bearer test_token"},
        json={"subscription_id": mock_subscription_dto.id},
    )

    removed = mock_subscription_dto.to_dict()
    removed["status"] = "removed"

    assert response.status_code == 200
    assert response.json() == {"subscription": removed}


def test_block_subscriber(client: TestClient, mock_subscription_dto: SubscriptionDTO) -> None:
    """Test blocking subscriber."""
    response = client.put(
        "/api/v1/subscription-management/block-subscriber",
        headers={"Authorization": "Bearer test_token"},
        json={"subscription_id": mock_subscription_dto.id},
    )

    blocked = mock_subscription_dto.to_dict()
    blocked["status"] = "blocked"

    assert response.status_code == 200
    assert response.json() == {"subscription": blocked}


def test_change_subscriber_role(client: TestClient, mock_subscription_dto: SubscriptionDTO) -> None:
    """Test changing subscriber role."""
    response = client.put(
        "/api/v1/subscription-management/update-role",
        headers={"Authorization": "Bearer test_token"},
        json={"subscription_id": mock_subscription_dto.id, "role": "birth_partner"},
    )

    birth_partner = mock_subscription_dto.to_dict()
    birth_partner["role"] = "birth_partner"

    assert response.status_code == 200
    assert response.json() == {"subscription": birth_partner}


def test_update_subscriber_contact_methods(
    client: TestClient,
    mock_subscription_dto: SubscriptionDTO,
) -> None:
    """Test updating subscriber contact methods."""
    response = client.put(
        "/api/v1/subscription-management/update-contact-methods",
        headers={"Authorization": "Bearer test_token"},
        json={"subscription_id": mock_subscription_dto.id, "contact_methods": ["sms"]},
    )

    contact_methods = mock_subscription_dto.to_dict()
    contact_methods["contact_methods"] = ["sms"]

    assert response.status_code == 200
    assert response.json() == {
        "subscription": contact_methods,
    }
