from fastapi.testclient import TestClient

from src.subscription.application.dtos import SubscriptionDTO


def test_webhook(client: TestClient) -> None:
    """Test handling a Stripe webhook."""
    response = client.post(
        "/api/v1/payments/webhook",
        headers={"stripe-signature": "test_signature"},
        content=b"test_payload",
    )

    assert response.status_code == 200


def test_create_checkout_session(
    client: TestClient,
    mock_subscription_dto: SubscriptionDTO,
) -> None:
    """Test creating a checkout session for inner circle upgrade."""
    response = client.post(
        "/api/v1/payments/create-checkout-session",
        headers={"Authorization": "Bearer test_token"},
        json={
            "subscription_id": mock_subscription_dto.id,
            "upgrade": "supporter",
            "success_url": "https://example.com/success",
            "cancel_url": "https://example.com/cancel",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": "test_session_id",
        "url": "https://test.stripe.com/checkout",
    }


def test_create_checkout_session_unauthorized(client: TestClient) -> None:
    """Test creating a checkout session without authorization."""
    response = client.post("/api/v1/payments/create-checkout-session")
    assert response.status_code == 403


def test_create_checkout_session_invalid_token(
    client: TestClient, mock_subscription_dto: SubscriptionDTO
) -> None:
    """Test creating a checkout session with invalid token."""
    response = client.post(
        "/api/v1/payments/create-checkout-session",
        headers={"Authorization": "Bearer invalid_token"},
        json={
            "subscription_id": mock_subscription_dto.id,
            "upgrade": "supporter",
            "success_url": "https://example.com/success",
            "cancel_url": "https://example.com/cancel",
        },
    )
    assert response.status_code == 401
