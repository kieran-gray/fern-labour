from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.enums import LabourPaymentPlan
from src.labour.domain.labour.exceptions import (
    CannotSubscribeToOwnLabour,
    InsufficientLabourPaymentPlan,
    InvalidLabourId,
    LabourNotFoundById,
    MaximumNumberOfSubscribersReached,
)
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from src.subscription.application.services.subscription_service import SubscriptionService
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import (
    SubscriberAlreadySubscribed,
    SubscriberIsBlocked,
    SubscriberNotSubscribed,
    SubscriptionTokenIncorrect,
)
from src.subscription.domain.repository import SubscriptionRepository
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "bp_id"
SUBSCRIBER = "subscriber_id"


@pytest_asyncio.fixture
async def subscription_service(
    labour_query_service: LabourQueryService,
    user_service: UserQueryService,
    subscription_repo: SubscriptionRepository,
    token_generator: TokenGenerator,
) -> SubscriptionService:
    await user_service._user_repository.save(
        User(
            id_=UserId(BIRTHING_PERSON),
            username="test789",
            first_name="user",
            last_name="name",
            email="test@birthing.com",
        )
    )
    await user_service._user_repository.save(
        User(
            id_=UserId(SUBSCRIBER),
            username="test456",
            first_name="sub",
            last_name="scriber",
            email="test@subscriber.com",
            phone_number="07123123123",
        )
    )
    return SubscriptionService(
        labour_query_service=labour_query_service,
        subscription_repository=subscription_repo,
        token_generator=token_generator,
        event_producer=AsyncMock(),
    )


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    return await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.COMMUNITY.value
    )


async def test_can_subscribe_to_labour(
    subscription_service: SubscriptionService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    subscriptions = await subscription_query_service.get_subscriber_subscriptions(
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

    subscriptions = await subscription_query_service.get_subscriber_subscriptions(
        subscriber_id=SUBSCRIBER
    )
    assert subscriptions == [subscription]


async def test_cannot_subscribe_to_labour_without_payment_plan(
    subscription_service: SubscriptionService, labour_service: LabourService
) -> None:
    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    token = subscription_service._token_generator.generate(labour.id)
    with pytest.raises(InsufficientLabourPaymentPlan):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
        )


async def test_cannot_subscribe_to_labour_with_solo_payment_plan(
    subscription_service: SubscriptionService, labour_service: LabourService
) -> None:
    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.SOLO.value
    )
    token = subscription_service._token_generator.generate(labour.id)
    with pytest.raises(InsufficientLabourPaymentPlan):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
        )


async def test_cannot_subscribe_to_labour_with_solo_payment_plan_sub_limit_reached(
    subscription_service: SubscriptionService,
    labour_service: LabourService,
    user_service: UserQueryService,
) -> None:
    user_ids = [str(uuid4()) for _ in range(5)]
    for user_id in user_ids:
        await user_service._user_repository.save(
            User(
                id_=UserId(user_id),
                username=user_id,
                first_name="user",
                last_name="name",
                email=f"{user_id}@sub.com",
            )
        )

    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.INNER_CIRCLE.value
    )
    token = subscription_service._token_generator.generate(labour.id)

    for user_id in user_ids:
        await subscription_service.subscribe_to(
            subscriber_id=user_id, labour_id=labour.id, token=token
        )

    with pytest.raises(MaximumNumberOfSubscribersReached):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
        )


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


async def test_cannot_subscribe_to_labour_invalid_id(
    subscription_service: SubscriptionService,
) -> None:
    token = subscription_service._token_generator.generate("test")

    with pytest.raises(InvalidLabourId):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id="test", token=token
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
    token = subscription_service._token_generator.generate(labour.id)

    with pytest.raises(CannotSubscribeToOwnLabour):
        await subscription_service.subscribe_to(
            subscriber_id=BIRTHING_PERSON, labour_id=labour.id, token=token
        )


async def test_cannot_subscribe_to_non_existent_labour(
    subscription_service: SubscriptionService,
) -> None:
    labour_id = str(uuid4())
    token = subscription_service._token_generator.generate(labour_id)
    with pytest.raises(LabourNotFoundById):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour_id, token=token
        )


async def test_cannot_subscribe_to_with_incorrect_token(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    with pytest.raises(SubscriptionTokenIncorrect):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour.id, token="INVALID"
        )


async def test_can_unsubscribe_from_labour(
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

    subscription = await subscription_service.unsubscribe_from(
        subscriber_id=SUBSCRIBER, labour_id=labour.id
    )
    assert subscription.status == SubscriptionStatus.UNSUBSCRIBED.value


async def test_cannot_unsubscribe_from_labour_twice(
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

    subscription = await subscription_service.unsubscribe_from(
        subscriber_id=SUBSCRIBER, labour_id=labour.id
    )
    assert subscription.status == SubscriptionStatus.UNSUBSCRIBED.value
    with pytest.raises(SubscriberNotSubscribed):
        await subscription_service.unsubscribe_from(subscriber_id=SUBSCRIBER, labour_id=labour.id)


async def test_cannot_unsubscribe_from_labour_invalid_id(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(InvalidLabourId):
        await subscription_service.unsubscribe_from(subscriber_id=SUBSCRIBER, labour_id="test")


async def test_cannot_unsubscribed_from_labour_not_subscribed_to(
    subscription_service: SubscriptionService,
    labour: LabourDTO,
) -> None:
    with pytest.raises(SubscriberNotSubscribed):
        await subscription_service.unsubscribe_from(subscriber_id=SUBSCRIBER, labour_id=labour.id)
