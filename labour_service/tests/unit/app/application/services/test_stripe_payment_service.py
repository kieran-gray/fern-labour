import logging
from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio
import stripe
from fern_labour_core.events.event_handler import EventHandler
from stripe import SignatureVerificationError

from src.payments.application.exceptions import (
    StripeProductNotFound,
    WebhookHasInvalidPayload,
    WebhookHasInvalidSignature,
    WebhookMissingSignatureHeader,
)
from src.payments.infrastructure.gateways.stripe.stripe_gateway import StripePaymentService

MODULE = "src.payments.infrastructure.gateways.stripe.stripe_gateway"


class MockEventHandler(EventHandler):
    async def handle(self, event):
        pass


@pytest_asyncio.fixture
def mock_event_handlers():
    return {"test.event": MockEventHandler()}


@pytest_asyncio.fixture
async def stripe_service(mock_event_handlers: dict[str, EventHandler]):
    return StripePaymentService(
        api_key="test_key",
        webhook_endpoint_secret="test_secret",
        event_handlers=mock_event_handlers,
    )


def test_stripe_payment_service_initialization(mock_event_handlers: dict[str, EventHandler]):
    """Test the initialization of StripePaymentService"""
    service = StripePaymentService(
        api_key="test_key",
        webhook_endpoint_secret="test_secret",
        event_handlers=mock_event_handlers,
    )

    assert service._api_key == "test_key"
    assert service._webhook_endpoint_secret == "test_secret"
    assert service._event_handlers == mock_event_handlers
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
            assert (
                "Received unknown.event event. Ignoring: No Event Handler Defined." in caplog.text
            )


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
