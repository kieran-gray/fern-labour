from datetime import UTC, datetime

import pytest
import pytest_asyncio

from src.labour.application.dtos.labour import LabourDTO
from src.labour.application.services.labour_service import LabourService
from src.labour.domain.labour.exceptions import (
    InvalidLabourId,
    UnauthorizedLabourRequest,
)
from src.subscription.application.security.subscription_authorization_service import (
    SubscriptionAuthorizationService,
)
from src.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from src.subscription.application.services.subscription_service import SubscriptionService
from src.subscription.domain.repository import SubscriptionRepository
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "bp_id"
SUBSCRIBER = "subscriber_id"


@pytest_asyncio.fixture
async def auth_service(
    user_service: UserQueryService,
    subscription_repo: SubscriptionRepository,
) -> SubscriptionAuthorizationService:
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
    return SubscriptionAuthorizationService(
        subscription_repository=subscription_repo,
    )


@pytest_asyncio.fixture
async def labour(labour_service: LabourService) -> LabourDTO:
    return await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )


async def test_can_user_access_labour_subscriber(
    auth_service: SubscriptionAuthorizationService,
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
    assert (
        await auth_service.ensure_can_access_labour(requester_id=SUBSCRIBER, labour_id=labour.id)
        is None
    )


async def test_cannot_access_labour_when_not_subscribed(
    auth_service: SubscriptionAuthorizationService, labour: LabourDTO
) -> None:
    with pytest.raises(UnauthorizedLabourRequest):
        await auth_service.ensure_can_access_labour(requester_id=SUBSCRIBER, labour_id=labour.id)


async def test_cannot_access_labour_invalid_id(
    auth_service: SubscriptionAuthorizationService,
) -> None:
    with pytest.raises(InvalidLabourId):
        await auth_service.ensure_can_access_labour(requester_id=SUBSCRIBER, labour_id="test")


async def test_cannot_access_labour_when_subscription_status_requested(
    auth_service: SubscriptionAuthorizationService,
    subscription_service: SubscriptionService,
    labour: LabourDTO,
) -> None:
    token = subscription_service._token_generator.generate(labour.id)
    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )
    with pytest.raises(UnauthorizedLabourRequest):
        await auth_service.ensure_can_access_labour(requester_id=SUBSCRIBER, labour_id=labour.id)


async def test_cannot_access_labour_when_subscription_status_unsubscribed(
    auth_service: SubscriptionAuthorizationService,
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
    await subscription_service.unsubscribe_from(subscriber_id=SUBSCRIBER, labour_id=labour.id)

    with pytest.raises(UnauthorizedLabourRequest):
        await auth_service.ensure_can_access_labour(requester_id=SUBSCRIBER, labour_id=labour.id)


async def test_cannot_access_labour_when_subscription_status_blocked(
    auth_service: SubscriptionAuthorizationService,
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
        await auth_service.ensure_can_access_labour(requester_id=SUBSCRIBER, labour_id=labour.id)


async def test_can_access_labour_when_subscription_status_removed(
    auth_service: SubscriptionAuthorizationService,
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
        await auth_service.ensure_can_access_labour(requester_id=SUBSCRIBER, labour_id=labour.id)
