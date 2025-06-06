from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.application.unit_of_work import UnitOfWork
from src.core.domain.domain_event.repository import DomainEventRepository
from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.exceptions import (
    CannotSubscribeToOwnLabour,
    InvalidLabourId,
    LabourNotFoundById,
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
    SubscriberAlreadyRequested,
    SubscriberAlreadySubscribed,
    SubscriberIsBlocked,
    SubscriberNotSubscribed,
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
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
    domain_event_repo: DomainEventRepository,
    unit_of_work: UnitOfWork,
    token_generator: TokenGenerator,
    domain_event_publisher: DomainEventPublisher,
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
        domain_event_repository=domain_event_repo,
        unit_of_work=unit_of_work,
        token_generator=token_generator,
        domain_event_publisher=domain_event_publisher,
    )


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    return await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
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
    assert subscription.status == SubscriptionStatus.REQUESTED.value

    subscriptions = await subscription_query_service.get_subscriber_subscriptions(
        subscriber_id=SUBSCRIBER
    )
    assert subscriptions == []


async def test_cannot_request_access_to_labour_more_than_once(
    subscription_service: SubscriptionService, labour: LabourDTO
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )

    with pytest.raises(SubscriberAlreadyRequested):
        await subscription_service.subscribe_to(
            subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
        )


async def test_cannot_request_access_to_subscribed_labour(
    subscription_service: SubscriptionService,
    subscription_management_service: SubscriptionManagementService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
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
    assert subscription.status == SubscriptionStatus.REQUESTED

    subscription = await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.SUBSCRIBED

    subscription = await subscription_management_service.remove_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.REMOVED

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    assert subscription.status == SubscriptionStatus.REQUESTED

    subscription = await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.SUBSCRIBED


async def test_can_subscribe_to_labour_when_unsubscribed(
    subscription_service: SubscriptionService,
    subscription_management_service: SubscriptionManagementService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    assert subscription.status == SubscriptionStatus.REQUESTED

    subscription = await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.SUBSCRIBED

    subscription = await subscription_service.unsubscribe_from(
        subscriber_id=SUBSCRIBER, labour_id=labour.id
    )
    assert subscription.status == SubscriptionStatus.UNSUBSCRIBED

    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    assert subscription.status == SubscriptionStatus.REQUESTED

    subscription = await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
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
    subscription_management_service: SubscriptionManagementService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription = await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
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
    subscription_management_service: SubscriptionManagementService,
    subscription_query_service: SubscriptionQueryService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    subscription = await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
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


async def test_ensure_can_update_access_level_success(
    subscription_service: SubscriptionService,
    subscription_management_service: SubscriptionManagementService,
    labour: LabourDTO,
):
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    await subscription_management_service.approve_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    await subscription_service.ensure_can_update_access_level(subscription_id=subscription.id)


async def test_ensure_can_update_access_level_not_subscribed(
    subscription_service: SubscriptionService, labour: LabourDTO
):
    token = subscription_service._token_generator.generate(labour.id)
    subscription = await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    with pytest.raises(SubscriberNotSubscribed):
        await subscription_service.ensure_can_update_access_level(subscription_id=subscription.id)


async def test_ensure_can_update_access_level_invalid_subscription_id(
    subscription_service: SubscriptionService,
):
    with pytest.raises(SubscriptionIdInvalid):
        await subscription_service.ensure_can_update_access_level(subscription_id="test")


async def test_ensure_can_update_access_level_subscription_not_found(
    subscription_service: SubscriptionService,
):
    with pytest.raises(SubscriptionNotFoundById):
        await subscription_service.ensure_can_update_access_level(subscription_id=str(uuid4()))
