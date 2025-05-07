import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock, patch
from uuid import UUID

import pytest
import pytest_asyncio
import stripe
from stripe import SignatureVerificationError

from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.labour_service import LabourService
from src.payments.infrastructure.stripe.exceptions import (
    StripeProductNotFound,
    WebhookHasInvalidPayload,
    WebhookHasInvalidSignature,
    WebhookMissingSignatureHeader,
)
from src.payments.infrastructure.stripe.product_mapping import Product
from src.payments.infrastructure.stripe.stripe_payment_service import StripePaymentService
from src.subscription.application.dtos import SubscriptionDTO
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.application.services.subscription_service import SubscriptionService
from src.subscription.domain.enums import SubscriptionAccessLevel
from src.subscription.domain.value_objects.subscription_id import SubscriptionId
from src.user.application.dtos.user import UserDTO
from src.user.domain.entity import User
from src.user.domain.repository import UserRepository
from src.user.domain.value_objects.user_id import UserId

MODULE = "src.payments.infrastructure.stripe.stripe_payment_service"
BIRTHING_PERSON = "bp_id"
SUBSCRIBER = "sub_id"


@dataclass
class MockProduct:
    metadata: dict[str, Any]
    default_price: str


@dataclass
class MockProductResponse:
    data: list[MockProduct]


@pytest_asyncio.fixture
async def stripe_service(subscription_management_service: SubscriptionManagementService):
    return StripePaymentService(
        api_key="test_key",
        webhook_endpoint_secret="test_secret",
        subscription_management_service=subscription_management_service,
    )


@pytest_asyncio.fixture
async def subscription(
    user_repo: UserRepository,
    labour_service: LabourService,
    subscription_service: SubscriptionService,
    token_generator: TokenGenerator,
) -> SubscriptionDTO:
    await user_repo.save(
        User(
            id_=UserId(BIRTHING_PERSON),
            username="test789",
            first_name="user",
            last_name="name",
            email="test@birthing.com",
        )
    )
    await user_repo.save(
        User(
            id_=UserId(SUBSCRIBER),
            username="test456",
            first_name="sub",
            last_name="scriber",
            email="test@subscriber.com",
            phone_number="07123123123",
        )
    )
    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    token = token_generator.generate(labour.id)
    return await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )


def test_stripe_payment_service_initialization(
    subscription_management_service: SubscriptionManagementService,
):
    """Test the initialization of StripePaymentService"""
    service = StripePaymentService(
        api_key="test_key",
        webhook_endpoint_secret="test_secret",
        subscription_management_service=subscription_management_service,
    )

    assert service._api_key == "test_key"
    assert service._webhook_endpoint_secret == "test_secret"
    assert service._stripe.api_key == "test_key"


async def test_generate_line_item_product_not_found(stripe_service: StripePaymentService):
    """Test generate_line_item raises StripeProductNotFound when product doesn't exist"""
    mock_products = MagicMock()
    mock_products.data = []

    with patch("stripe.Product.list_async", return_value=mock_products):
        with pytest.raises(StripeProductNotFound):
            await stripe_service.generate_line_item("nonexistent_item")


async def test_handle_webhook_missing_signature(stripe_service: StripePaymentService):
    """Test handle_webhook raises WebhookMissingSignatureHeader when signature is missing"""
    with pytest.raises(WebhookMissingSignatureHeader):
        await stripe_service.handle_webhook(payload=b"test", signature_header=None)


async def test_handle_webhook_invalid_payload(stripe_service: StripePaymentService):
    """Test handle_webhook raises WebhookHasInvalidPayload for invalid payload"""
    with patch.object(stripe.Webhook, "construct_event", side_effect=ValueError):
        with pytest.raises(WebhookHasInvalidPayload):
            await stripe_service.handle_webhook(
                payload=b"invalid_payload", signature_header="test_signature"
            )


async def test_handle_webhook_invalid_signature(stripe_service: StripePaymentService):
    """Test handle_webhook raises WebhookHasInvalidSignature for invalid signature"""
    with patch.object(
        stripe.Webhook,
        "construct_event",
        side_effect=SignatureVerificationError("message", "sig_header"),
    ):
        with pytest.raises(WebhookHasInvalidSignature):
            await stripe_service.handle_webhook(
                payload=b"test_payload", signature_header="invalid_signature"
            )


async def test_handle_webhook_valid_event_with_handler(stripe_service: StripePaymentService):
    """Test handle_webhook processes valid event with registered handler"""
    mock_event = {"type": "test.event", "data": "test_data"}

    with patch.object(stripe.Webhook, "construct_event", return_value=mock_event):
        await stripe_service.handle_webhook(
            payload=b"test_payload", signature_header="valid_signature"
        )


async def test_handle_webhook_valid_event_without_handler(
    stripe_service: StripePaymentService, caplog: pytest.LogCaptureFixture
):
    """Test handle_webhook logs info when no handler is registered for event type"""
    mock_event = {"type": "unknown.event", "data": "test_data"}

    with patch.object(stripe.Webhook, "construct_event", return_value=mock_event):
        with caplog.at_level(logging.INFO, MODULE):
            await stripe_service.handle_webhook(
                payload=b"test_payload", signature_header="valid_signature"
            )
            assert "Received unknown.event event. Ignoring." in caplog.text


async def test_generate_line_item_success(stripe_service: StripePaymentService):
    """Test successful generation of line item"""
    mock_product = MagicMock()
    mock_product.metadata = {"product": "test_item"}
    mock_product.default_price = "price_123"

    mock_products = MagicMock()
    mock_products.data = [mock_product]

    with patch("stripe.Product.list_async", return_value=mock_products):
        line_item = await stripe_service.generate_line_item("test_item")
        assert line_item == {"price": "price_123", "quantity": 1}


async def test_handle_successful_checkout_session_webhook(
    stripe_service: StripePaymentService,
    subscription: SubscriptionDTO,
):
    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"subscription_id": subscription.id},
            }
        },
        "type": "checkout.session.completed",
    }

    mock_stripe = MagicMock()
    mock_stripe.Webhook.construct_event = Mock(return_value=event)
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(data=[MagicMock(price=MagicMock(product="prod_123"))]),
    )
    mock_stripe.Product.retrieve_async = AsyncMock(
        return_value=MagicMock(metadata={"product": Product.UPGRADE_TO_SUPPORTER.value})
    )
    stripe_service._stripe = mock_stripe

    await stripe_service.handle_webhook(payload=b"test_payload", signature_header="valid_signature")
    sub_mgmt_service = stripe_service._subscription_management_service
    domain_subscription = await sub_mgmt_service._subscription_repository.get_by_id(
        SubscriptionId(UUID(subscription.id))
    )
    assert domain_subscription.access_level is SubscriptionAccessLevel.SUPPORTER


async def test_handle_successful_checkout_session(
    stripe_service: StripePaymentService,
    subscription: SubscriptionDTO,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(data=[MagicMock(price=MagicMock(product="prod_123"))]),
    )
    mock_stripe.Product.retrieve_async = AsyncMock(
        return_value=MagicMock(metadata={"product": Product.UPGRADE_TO_SUPPORTER.value})
    )

    stripe_service._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"subscription_id": subscription.id},
            }
        }
    }

    await stripe_service.complete_checkout_session(event)
    sub_mgmt_service = stripe_service._subscription_management_service
    domain_subscription = await sub_mgmt_service._subscription_repository.get_by_id(
        SubscriptionId(UUID(subscription.id))
    )
    assert domain_subscription.access_level is SubscriptionAccessLevel.SUPPORTER


async def test_handle_no_line_items(
    stripe_service: StripePaymentService,
    subscription: SubscriptionDTO,
    caplog: pytest.LogCaptureFixture,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid", line_items=None
    )

    stripe_service._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"subscription_id": subscription.id},
            }
        }
    }
    with caplog.at_level(logging.ERROR, MODULE):
        await stripe_service.complete_checkout_session(event)
        assert len(caplog.records) == 1
        assert "No line items found" in caplog.messages[0]


async def test_handle_multiple_line_items(
    stripe_service: StripePaymentService,
    subscription: SubscriptionDTO,
    caplog: pytest.LogCaptureFixture,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(
            data=[
                MagicMock(price=MagicMock(product="prod_123")),
                MagicMock(price=MagicMock(product="prod_abc")),
                MagicMock(price=MagicMock(product="prod_999")),
            ]
        ),
    )

    mock_stripe.Product.retrieve_async = AsyncMock(
        return_value=MagicMock(metadata={"product": Product.UPGRADE_TO_SUPPORTER.value})
    )

    stripe_service._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"subscription_id": subscription.id},
            }
        }
    }
    with caplog.at_level(logging.ERROR, MODULE):
        await stripe_service.complete_checkout_session(event)
        assert len(caplog.records) == 1
        assert "Multiple line items found" in caplog.messages[0]

    sub_mgmt_service = stripe_service._subscription_management_service
    domain_subscription = await sub_mgmt_service._subscription_repository.get_by_id(
        SubscriptionId(UUID(subscription.id))
    )
    assert domain_subscription.access_level is SubscriptionAccessLevel.SUPPORTER


async def test_handle_no_price_in_line_item(
    stripe_service: StripePaymentService,
    subscription: SubscriptionDTO,
    caplog: pytest.LogCaptureFixture,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(data=[MagicMock(price=None)]),
    )

    stripe_service._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"subscription_id": subscription.id},
            }
        }
    }

    with caplog.at_level(logging.ERROR, MODULE):
        await stripe_service.complete_checkout_session(event)
        assert len(caplog.records) == 1
        assert "No price ID found" in caplog.messages[0]


async def test_handle_no_product_metadata(
    stripe_service: StripePaymentService,
    subscription: SubscriptionDTO,
    caplog: pytest.LogCaptureFixture,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(data=[MagicMock(price=MagicMock(product="prod_123"))]),
    )
    mock_stripe.Product.retrieve_async = AsyncMock(return_value=MagicMock(metadata={}))

    stripe_service._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"subscription_id": subscription.id},
            }
        }
    }
    with caplog.at_level(logging.ERROR, MODULE):
        await stripe_service.complete_checkout_session(event)
        assert len(caplog.records) == 1
        assert "No product metadata for price" in caplog.messages[0]

    sub_mgmt_service = stripe_service._subscription_management_service
    domain_subscription = await sub_mgmt_service._subscription_repository.get_by_id(
        SubscriptionId(UUID(subscription.id))
    )
    assert domain_subscription.access_level is SubscriptionAccessLevel.SUPPORTER


async def test_checkout_session_product_not_in_mapping(
    stripe_service: StripePaymentService,
    subscription: SubscriptionDTO,
    caplog: pytest.LogCaptureFixture,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(data=[MagicMock(price=MagicMock(product="prod_123"))]),
    )
    mock_stripe.Product.retrieve_async = AsyncMock(
        return_value=MagicMock(metadata={"product": "test_product"})
    )

    stripe_service._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"subscription_id": subscription.id},
            }
        }
    }

    with caplog.at_level(logging.ERROR, MODULE):
        await stripe_service.complete_checkout_session(event)
        assert len(caplog.records) == 1
        assert "No access level found for test_product" in caplog.messages[0]

    sub_mgmt_service = stripe_service._subscription_management_service
    domain_subscription = await sub_mgmt_service._subscription_repository.get_by_id(
        SubscriptionId(UUID(subscription.id))
    )
    assert domain_subscription.access_level is SubscriptionAccessLevel.SUPPORTER


async def test_create_checkout_session(
    stripe_service: StripePaymentService,
    subscription: SubscriptionDTO,
):
    mock_stripe = MagicMock()
    checkout_session_mock = Mock()
    mock_stripe.checkout.Session.create = checkout_session_mock
    response = MockProductResponse(
        data=[MockProduct(metadata={"product": "test"}, default_price="$69")]
    )
    mock_stripe.Product.list_async = AsyncMock(return_value=response)
    stripe_service._stripe = mock_stripe
    user = UserDTO(
        id="test_id",
        username="test123",
        first_name="User",
        last_name="Name",
        email="test@email.com",
        phone_number="+44123123123",
    )
    await stripe_service.create_checkout_session(
        user=user,
        success_url="https://test.com",
        cancel_url="https://cancel.com",
        item="test",
        subscription_id=subscription.id,
    )
    checkout_session_mock.assert_called_once()
