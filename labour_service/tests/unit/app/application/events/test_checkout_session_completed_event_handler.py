import logging
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.enums import LabourPaymentPlan
from src.payments.application.event_handlers.checkout_session_completed_event_handler import (
    CheckoutSessionCompletedEventHandler,
)
from src.payments.infrastructure.gateways.stripe.product_mapping import Product
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "bp_id"
MODULE = "src.payments.application.event_handlers.checkout_session_completed_event_handler"


@pytest_asyncio.fixture
async def checkout_session_completed_event_handler(
    labour_service: LabourService,
) -> CheckoutSessionCompletedEventHandler:
    await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    return CheckoutSessionCompletedEventHandler(api_key="test", labour_service=labour_service)


async def test_handle_successful_checkout_session(
    checkout_session_completed_event_handler: CheckoutSessionCompletedEventHandler,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(data=[MagicMock(price=MagicMock(product="prod_123"))]),
    )
    mock_stripe.Product.retrieve_async = AsyncMock(
        return_value=MagicMock(metadata={"product": Product.UPGRADE_TO_COMMUNITY.value})
    )

    checkout_session_completed_event_handler._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"user_id": BIRTHING_PERSON},
            }
        }
    }

    await checkout_session_completed_event_handler.handle(event)
    labour_repo = checkout_session_completed_event_handler._labour_service._labour_repository
    labour = await labour_repo.get_active_labour_by_birthing_person_id(
        birthing_person_id=UserId(BIRTHING_PERSON)
    )
    assert labour.payment_plan is LabourPaymentPlan.COMMUNITY


async def test_handle_no_line_items(
    checkout_session_completed_event_handler: CheckoutSessionCompletedEventHandler,
    caplog: pytest.LogCaptureFixture,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid", line_items=None
    )

    checkout_session_completed_event_handler._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"user_id": BIRTHING_PERSON},
            }
        }
    }
    with caplog.at_level(logging.ERROR, MODULE):
        await checkout_session_completed_event_handler.handle(event)
        assert len(caplog.records) == 1
        assert "No line items found" in caplog.messages[0]


async def test_handle_multiple_line_items(
    checkout_session_completed_event_handler: CheckoutSessionCompletedEventHandler,
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
        return_value=MagicMock(metadata={"product": Product.UPGRADE_TO_COMMUNITY.value})
    )

    checkout_session_completed_event_handler._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"user_id": BIRTHING_PERSON},
            }
        }
    }
    with caplog.at_level(logging.ERROR, MODULE):
        await checkout_session_completed_event_handler.handle(event)
        assert len(caplog.records) == 1
        assert "Multiple line items found" in caplog.messages[0]

    labour_repo = checkout_session_completed_event_handler._labour_service._labour_repository
    labour = await labour_repo.get_active_labour_by_birthing_person_id(
        birthing_person_id=UserId(BIRTHING_PERSON)
    )
    assert labour.payment_plan is LabourPaymentPlan.COMMUNITY


async def test_handle_no_price_in_line_item(
    checkout_session_completed_event_handler: CheckoutSessionCompletedEventHandler,
    caplog: pytest.LogCaptureFixture,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(data=[MagicMock(price=None)]),
    )

    checkout_session_completed_event_handler._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"user_id": BIRTHING_PERSON},
            }
        }
    }

    with caplog.at_level(logging.ERROR, MODULE):
        await checkout_session_completed_event_handler.handle(event)
        assert len(caplog.records) == 1
        assert "No price ID found" in caplog.messages[0]


async def test_handle_no_product_metadata(
    checkout_session_completed_event_handler: CheckoutSessionCompletedEventHandler,
    caplog: pytest.LogCaptureFixture,
):
    mock_stripe = MagicMock()
    mock_stripe.checkout.Session.retrieve.return_value = MagicMock(
        payment_status="paid",
        line_items=MagicMock(data=[MagicMock(price=MagicMock(product="prod_123"))]),
    )
    mock_stripe.Product.retrieve_async = AsyncMock(return_value=MagicMock(metadata={}))

    checkout_session_completed_event_handler._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"user_id": BIRTHING_PERSON},
            }
        }
    }
    with caplog.at_level(logging.ERROR, MODULE):
        await checkout_session_completed_event_handler.handle(event)
        assert len(caplog.records) == 1
        assert "No product metadata for price" in caplog.messages[0]

    labour_repo = checkout_session_completed_event_handler._labour_service._labour_repository
    labour = await labour_repo.get_active_labour_by_birthing_person_id(
        birthing_person_id=UserId(BIRTHING_PERSON)
    )
    assert labour.payment_plan is LabourPaymentPlan.COMMUNITY


async def test_checkout_session_product_not_in_mapping(
    checkout_session_completed_event_handler: CheckoutSessionCompletedEventHandler,
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

    checkout_session_completed_event_handler._stripe = mock_stripe

    event = {
        "data": {
            "object": {
                "id": "session_123",
                "metadata": {"user_id": BIRTHING_PERSON},
            }
        }
    }

    with caplog.at_level(logging.ERROR, MODULE):
        await checkout_session_completed_event_handler.handle(event)
        assert len(caplog.records) == 1
        assert "No payment plan found for test_product" in caplog.messages[0]

    labour_repo = checkout_session_completed_event_handler._labour_service._labour_repository
    labour = await labour_repo.get_active_labour_by_birthing_person_id(
        birthing_person_id=UserId(BIRTHING_PERSON)
    )
    assert labour.payment_plan is LabourPaymentPlan.COMMUNITY
