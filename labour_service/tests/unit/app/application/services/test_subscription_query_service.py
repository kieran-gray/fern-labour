from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from app.labour.application.dtos.labour import LabourDTO
from app.labour.application.services.labour_service import LabourService
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.subscription.application.dtos.subscription import SubscriptionDTO
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.subscription.application.services.subscription_service import SubscriptionService
from app.subscription.domain.exceptions import (
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
    UnauthorizedSubscriptionRequest,
)

BIRTHING_PERSON = "bp_id"
SUBSCRIBER = "subscriber_id"


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    return await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.COMMUNITY.value
    )


async def test_can_get_subscription_by_id(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription_by_id = await subscription_query_service.get_by_id(
        requester_id=SUBSCRIBER, subscription_id=subscription.id
    )
    assert isinstance(subscription_by_id, SubscriptionDTO)
    assert subscription == subscription_by_id


async def test_cannot_get_subscription_by_id_as_subscriber_when_not_subscribed(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_service.unsubscribe_from(subscriber_id=SUBSCRIBER, labour_id=labour.id)
    with pytest.raises(UnauthorizedSubscriptionRequest):
        await subscription_query_service.get_by_id(
            requester_id=SUBSCRIBER, subscription_id=subscription.id
        )


async def test_can_get_subscription_by_id_as_birthing_person_when_not_subscribed(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription = await subscription_service.unsubscribe_from(
        subscriber_id=SUBSCRIBER, labour_id=labour.id
    )
    subscription_by_id = await subscription_query_service.get_by_id(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert isinstance(subscription_by_id, SubscriptionDTO)
    assert subscription == subscription_by_id


async def test_can_get_subscription_by_id_request_by_birthing_person(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription_by_id = await subscription_query_service.get_by_id(
        requester_id=labour.birthing_person_id, subscription_id=subscription.id
    )
    assert isinstance(subscription_by_id, SubscriptionDTO)
    assert subscription == subscription_by_id


async def test_cannot_get_subscription_with_invalid_id(
    subscription_query_service: SubscriptionQueryService,
) -> None:
    with pytest.raises(SubscriptionIdInvalid):
        await subscription_query_service.get_by_id(requester_id=SUBSCRIBER, subscription_id="test")


async def test_cannot_get_non_existent_subscription(
    subscription_query_service: SubscriptionQueryService,
) -> None:
    with pytest.raises(SubscriptionNotFoundById):
        await subscription_query_service.get_by_id(
            requester_id=SUBSCRIBER, subscription_id=str(uuid4())
        )


async def test_cannot_get_subscription_if_not_subscriber_or_birthing_person(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    with pytest.raises(UnauthorizedSubscriptionRequest):
        await subscription_query_service.get_by_id(
            requester_id=str(uuid4()), subscription_id=subscription.id
        )


async def test_can_query_own_subscriptions(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscriptions = await subscription_query_service.get_subscriber_subscriptions(
        subscriber_id=SUBSCRIBER
    )
    assert subscriptions == [subscription]


async def test_can_query_subscriptions_for_own_labour(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscriptions = await subscription_query_service.get_labour_subscriptions(
        requester_id=BIRTHING_PERSON, labour_id=labour.id
    )
    assert subscriptions == [subscription]


async def test_cannot_query_subscriptions_for_other_labour(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscriptions = await subscription_query_service.get_labour_subscriptions(
        requester_id=SUBSCRIBER, labour_id=labour.id
    )
    assert subscriptions == []
