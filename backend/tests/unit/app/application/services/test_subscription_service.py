from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from app.application.dtos.labour import LabourDTO
from app.application.security.token_generator import TokenGenerator
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_service import LabourService
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_management_service import SubscriptionManagementService
from app.application.services.subscription_service import SubscriptionService
from app.domain.labour.exceptions import LabourNotFoundById
from app.domain.subscriber.exceptions import SubscriberCannotSubscribeToSelf, SubscriberNotFoundById
from app.domain.subscription.enums import SubscriptionStatus
from app.domain.subscription.exceptions import (
    SubscriberAlreadySubscribed,
    SubscriberIsBlocked,
    SubscriberNotSubscribed,
    SubscriptionTokenIncorrect,
    UnauthorizedSubscriptionRequest,
)
from app.domain.subscription.repository import SubscriptionRepository

BIRTHING_PERSON = "bp_id"
SUBSCRIBER = "subscriber_id"


@pytest_asyncio.fixture
async def subscription_service(
    get_labour_service: GetLabourService,
    birthing_person_service: BirthingPersonService,
    subscriber_service: SubscriberService,
    subscription_repo: SubscriptionRepository,
    token_generator: TokenGenerator,
) -> SubscriptionService:
    await birthing_person_service.register(
        birthing_person_id=BIRTHING_PERSON,
        first_name="Name",
        last_name="User",
    )
    await subscriber_service.register(
        subscriber_id=SUBSCRIBER,
        first_name="First",
        last_name="Last",
        phone_number="07123123123",
        email="test@email.com",
    )
    return SubscriptionService(
        get_labour_service=get_labour_service,
        subscriber_service=subscriber_service,
        subscription_repository=subscription_repo,
        token_generator=token_generator,
        event_producer=AsyncMock(),
    )


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    return await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )


async def test_can_subscribe_to_labour(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    subscriptions = await subscription_service.get_subscriber_subscriptions(
        subscriber_id=SUBSCRIBER
    )
    assert subscriptions == []

    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    assert subscription.birthing_person_id == BIRTHING_PERSON
    assert subscription.labour_id == labour.id
    assert subscription.subscriber_id == SUBSCRIBER
    assert subscription.status == SubscriptionStatus.SUBSCRIBED.value

    subscriptions = await subscription_service.get_subscriber_subscriptions(
        subscriber_id=SUBSCRIBER
    )
    assert subscriptions == [subscription]


async def test_cannot_subscribe_to_labour_more_than_once(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )

    with pytest.raises(SubscriberAlreadySubscribed):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
        )


async def test_can_subscribe_to_labour_when_removed(
    subscription_service: SubscriptionService,
    subscription_management_service: SubscriptionManagementService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription = await subscription_management_service.remove_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.REMOVED

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    assert subscription.status == SubscriptionStatus.SUBSCRIBED


async def test_can_subscribe_to_labour_when_unsubscribed(
    subscription_service: SubscriptionService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription = await subscription_service.unsubscribe_from(
        subscriber_id=SUBSCRIBER, labour_id=labour.id
    )
    assert subscription.status == SubscriptionStatus.UNSUBSCRIBED

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    assert subscription.status == SubscriptionStatus.SUBSCRIBED


async def test_cannot_subscribe_to_labour_when_blocked(
    subscription_service: SubscriptionService,
    subscription_management_service: SubscriptionManagementService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.block_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )

    with pytest.raises(SubscriberIsBlocked):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
        )


async def test_cannot_subscribe_to_own_labour(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    await subscription_service._subscriber_service.register(
        subscriber_id=BIRTHING_PERSON, first_name="test", last_name="user"
    )
    token = subscription_service._token_generator.generate(labour.id)

    with pytest.raises(SubscriberCannotSubscribeToSelf):
        await subscription_service.subscribe_to(
            subscriber_id=BIRTHING_PERSON, labour_id=labour.id, token=token
        )


async def test_cannot_subscribe_to_non_existent_labour(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(LabourNotFoundById):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=str(uuid4()), token="test"
        )


async def test_cannot_subscribe_with_non_existent_subscriber(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    with pytest.raises(SubscriberNotFoundById):
        await subscription_service.subscribe_to("TEST", labour_id=labour.id, token=token)


async def test_cannot_subscribe_to_with_incorrect_token(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    with pytest.raises(SubscriptionTokenIncorrect):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour.id, token="INVALID"
        )


async def test_can_unsubscribe_from_labour(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscriptions = await subscription_service.get_subscriber_subscriptions(
        subscriber_id=SUBSCRIBER
    )
    assert subscriptions == [subscription]

    subscription = await subscription_service.unsubscribe_from(
        subscriber_id=SUBSCRIBER, labour_id=labour.id
    )
    assert subscription.status == SubscriptionStatus.UNSUBSCRIBED.value


async def test_cannot_unsubscribe_from_labour_twice(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscriptions = await subscription_service.get_subscriber_subscriptions(
        subscriber_id=SUBSCRIBER
    )
    assert subscriptions == [subscription]

    subscription = await subscription_service.unsubscribe_from(
        subscriber_id=SUBSCRIBER, labour_id=labour.id
    )
    assert subscription.status == SubscriptionStatus.UNSUBSCRIBED.value
    with pytest.raises(SubscriberNotSubscribed):
        await subscription_service.unsubscribe_from(subscriber_id=SUBSCRIBER, labour_id=labour.id)


async def test_cannot_unsubscribed_from_labour_not_subscribed_to(
    subscription_service: SubscriptionService,
    labour: LabourDTO,
) -> None:
    with pytest.raises(SubscriberNotSubscribed):
        await subscription_service.unsubscribe_from(subscriber_id=SUBSCRIBER, labour_id=labour.id)


async def test_cannot_unsubscribe_with_non_existent_subscriber(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    with pytest.raises(SubscriberNotFoundById):
        await subscription_service.unsubscribe_from(subscriber_id="TEST", labour_id=labour.id)


async def test_can_query_own_subscriptions(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscriptions = await subscription_service.get_subscriber_subscriptions(
        subscriber_id=SUBSCRIBER
    )
    assert subscriptions == [subscription]


async def test_can_query_subscriptions_for_own_labour(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscriptions = await subscription_service.get_labour_subscriptions(
        requester_id=BIRTHING_PERSON, labour_id=labour.id
    )
    assert subscriptions == [subscription]


async def test_cannot_query_subscriptions_for_other_labour(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    with pytest.raises(UnauthorizedSubscriptionRequest):
        await subscription_service.get_labour_subscriptions(
            requester_id=SUBSCRIBER, labour_id=labour.id
        )


async def test_can_query_subscribers_for_own_labour(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscriber = await subscription_service._subscriber_service.get(subscriber_id=SUBSCRIBER)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscribers = await subscription_service.get_labour_subscribers(
        requester_id=BIRTHING_PERSON, labour_id=labour.id
    )
    assert subscribers == [subscriber]


async def test_cannot_query_subscribers_for_other_labour(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    with pytest.raises(UnauthorizedSubscriptionRequest):
        await subscription_service.get_labour_subscribers(
            requester_id=SUBSCRIBER, labour_id=labour.id
        )
