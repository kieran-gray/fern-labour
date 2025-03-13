from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from app.application.dtos.labour import LabourDTO
from app.application.dtos.subscription import SubscriptionDTO
from app.application.security.token_generator import TokenGenerator
from app.application.services.get_labour_service import GetLabourService
from app.application.services.labour_service import LabourService
from app.application.services.subscription_management_service import SubscriptionManagementService
from app.application.services.subscription_service import SubscriptionService
from app.application.services.user_service import UserService
from app.domain.labour.enums import LabourPaymentPlan
from app.domain.labour.exceptions import LabourNotFoundById, UnauthorizedLabourRequest
from app.domain.subscription.enums import SubscriptionStatus
from app.domain.subscription.exceptions import (
    SubscriberAlreadySubscribed,
    SubscriberIsBlocked,
    SubscriberNotSubscribed,
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
    SubscriptionTokenIncorrect,
    UnauthorizedSubscriptionRequest,
)
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.user.entity import User
from app.domain.user.exceptions import UserCannotSubscribeToSelf, UserNotFoundById
from app.domain.user.vo_user_id import UserId

BIRTHING_PERSON = "bp_id"
SUBSCRIBER = "subscriber_id"


@pytest_asyncio.fixture
async def subscription_service(
    get_labour_service: GetLabourService,
    user_service: UserService,
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
        get_labour_service=get_labour_service,
        user_service=user_service,
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


async def test_can_get_subscription_by_id(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription_by_id = await subscription_service.get_by_id(
        requester_id=SUBSCRIBER, subscription_id=subscription.id
    )
    assert isinstance(subscription_by_id, SubscriptionDTO)
    assert subscription == subscription_by_id


async def test_can_get_subscription_by_id_request_by_birthing_person(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription_by_id = await subscription_service.get_by_id(
        requester_id=labour.birthing_person_id, subscription_id=subscription.id
    )
    assert isinstance(subscription_by_id, SubscriptionDTO)
    assert subscription == subscription_by_id


async def test_cannot_get_subscription_with_invalid_id(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(SubscriptionIdInvalid):
        await subscription_service.get_by_id(requester_id=SUBSCRIBER, subscription_id="test")


async def test_cannot_get_non_existent_subscription(
    subscription_service: SubscriptionService,
) -> None:
    with pytest.raises(SubscriptionNotFoundById):
        await subscription_service.get_by_id(requester_id=SUBSCRIBER, subscription_id=str(uuid4()))


async def test_cannot_get_subscription_if_not_subscriber_or_birthing_person(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    with pytest.raises(UnauthorizedSubscriptionRequest):
        await subscription_service.get_by_id(
            requester_id=str(uuid4()), subscription_id=subscription.id
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

    with pytest.raises(UserCannotSubscribeToSelf):
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
    with pytest.raises(UserNotFoundById):
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
    with pytest.raises(UserNotFoundById):
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


async def test_can_user_access_labour_subscriber(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    assert await subscription_service.can_user_access_labour(
        requester_id=SUBSCRIBER, labour_id=labour.id
    )


async def test_cannot_access_labour_when_not_subscribed(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    with pytest.raises(UnauthorizedLabourRequest):
        await subscription_service.can_user_access_labour(
            requester_id=SUBSCRIBER, labour_id=labour.id
        )


async def test_cannot_access_labour_when_subscription_status_unsubscribed(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_service.unsubscribe_from(subscriber_id=SUBSCRIBER, labour_id=labour.id)

    with pytest.raises(UnauthorizedLabourRequest):
        await subscription_service.can_user_access_labour(
            requester_id=SUBSCRIBER, labour_id=labour.id
        )


async def test_cannot_access_labour_when_subscription_status_blocked(
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
    with pytest.raises(UnauthorizedLabourRequest):
        await subscription_service.can_user_access_labour(
            requester_id=SUBSCRIBER, labour_id=labour.id
        )


async def test_can_access_labour_when_subscription_status_removed(
    subscription_service: SubscriptionService,
    subscription_management_service: SubscriptionManagementService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.remove_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    with pytest.raises(UnauthorizedLabourRequest):
        await subscription_service.can_user_access_labour(
            requester_id=SUBSCRIBER, labour_id=labour.id
        )


async def test_can_user_access_labour_own_labour(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    assert await subscription_service.can_user_access_labour(
        requester_id=BIRTHING_PERSON, labour_id=labour.id
    )
