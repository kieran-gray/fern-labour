from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from app.labour.application.dtos.subscription import SubscriptionDTO
from app.labour.application.security.token_generator import TokenGenerator
from app.labour.application.services.labour_service import LabourService
from app.labour.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from app.labour.application.services.subscription_service import SubscriptionService
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.labour.domain.subscription.enums import ContactMethod, SubscriberRole, SubscriptionStatus
from app.labour.domain.subscription.exceptions import (
    SubscriberRoleInvalid,
    SubscriptionContactMethodInvalid,
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
    UnauthorizedSubscriptionUpdateRequest,
)
from app.user.application.services.user_service import UserService
from app.user.domain.entity import User
from app.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "bp_id"
SUBSCRIBER = "subscriber_id"


@pytest_asyncio.fixture
async def subscription(
    user_service: UserService,
    labour_service: LabourService,
    subscription_service: SubscriptionService,
    token_generator: TokenGenerator,
) -> SubscriptionDTO:
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
    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.COMMUNITY.value
    )
    token = token_generator.generate(labour.id)
    return await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )


async def test_can_remove_subscriber(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    subscription = await subscription_management_service.remove_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.REMOVED


async def test_can_remove_subscriber_twice(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    subscription = await subscription_management_service.remove_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.REMOVED

    subscription = await subscription_management_service.remove_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.REMOVED


async def test_only_birthing_person_can_remove_subscriber(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    with pytest.raises(UnauthorizedSubscriptionUpdateRequest):
        await subscription_management_service.remove_subscriber(
            requester_id=SUBSCRIBER, subscription_id=subscription.id
        )


async def test_invalid_id_raises_error_remove(
    subscription_management_service: SubscriptionManagementService,
) -> None:
    with pytest.raises(SubscriptionIdInvalid):
        await subscription_management_service.remove_subscriber(
            requester_id=SUBSCRIBER, subscription_id="test-id"
        )


async def test_cannot_remove_from_non_existent_subscription(
    subscription_management_service: SubscriptionManagementService,
) -> None:
    with pytest.raises(SubscriptionNotFoundById):
        await subscription_management_service.remove_subscriber(
            requester_id=SUBSCRIBER, subscription_id=str(uuid4())
        )


async def test_can_block_subscriber(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    subscription = await subscription_management_service.block_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.BLOCKED


async def test_can_block_subscriber_twice(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    subscription = await subscription_management_service.block_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.BLOCKED

    subscription = await subscription_management_service.block_subscriber(
        requester_id=BIRTHING_PERSON, subscription_id=subscription.id
    )
    assert subscription.status == SubscriptionStatus.BLOCKED


async def test_only_birthing_person_can_block_subscriber(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    with pytest.raises(UnauthorizedSubscriptionUpdateRequest):
        await subscription_management_service.block_subscriber(
            requester_id=SUBSCRIBER, subscription_id=subscription.id
        )


async def test_invalid_id_raises_error_block(
    subscription_management_service: SubscriptionManagementService,
) -> None:
    with pytest.raises(SubscriptionIdInvalid):
        await subscription_management_service.block_subscriber(
            requester_id=SUBSCRIBER, subscription_id="test-id"
        )


async def test_cannot_block_for_non_existent_subscription(
    subscription_management_service: SubscriptionManagementService,
) -> None:
    with pytest.raises(SubscriptionNotFoundById):
        await subscription_management_service.block_subscriber(
            requester_id=SUBSCRIBER, subscription_id=str(uuid4())
        )


async def test_can_update_subscriber_role(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    assert subscription.role == SubscriberRole.FRIENDS_AND_FAMILY
    subscription = await subscription_management_service.update_role(
        requester_id=BIRTHING_PERSON,
        subscription_id=subscription.id,
        role=SubscriberRole.BIRTH_PARTNER,
    )
    assert subscription.role == SubscriberRole.BIRTH_PARTNER


async def test_can_update_subscriber_role_twice(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    assert subscription.role == SubscriberRole.FRIENDS_AND_FAMILY
    subscription = await subscription_management_service.update_role(
        requester_id=BIRTHING_PERSON,
        subscription_id=subscription.id,
        role=SubscriberRole.BIRTH_PARTNER,
    )
    assert subscription.role == SubscriberRole.BIRTH_PARTNER
    subscription = await subscription_management_service.update_role(
        requester_id=BIRTHING_PERSON,
        subscription_id=subscription.id,
        role=SubscriberRole.BIRTH_PARTNER,
    )
    assert subscription.role == SubscriberRole.BIRTH_PARTNER


async def test_cannot_update_subscriber_role_with_invalid_value(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    with pytest.raises(SubscriberRoleInvalid):
        await subscription_management_service.update_role(
            requester_id=BIRTHING_PERSON,
            subscription_id=subscription.id,
            role="wah",
        )


async def test_only_birthing_person_can_update_subscriber_role(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    with pytest.raises(UnauthorizedSubscriptionUpdateRequest):
        await subscription_management_service.update_role(
            requester_id=SUBSCRIBER,
            subscription_id=subscription.id,
            role=SubscriberRole.BIRTH_PARTNER,
        )


async def test_invalid_id_raises_error_update_role(
    subscription_management_service: SubscriptionManagementService,
) -> None:
    with pytest.raises(SubscriptionIdInvalid):
        await subscription_management_service.update_role(
            requester_id=SUBSCRIBER,
            subscription_id="test",
            role=SubscriberRole.BIRTH_PARTNER,
        )


async def test_cannot_update_role_for_non_existent_subscription(
    subscription_management_service: SubscriptionManagementService,
) -> None:
    with pytest.raises(SubscriptionNotFoundById):
        await subscription_management_service.update_role(
            requester_id=SUBSCRIBER,
            subscription_id=str(uuid4()),
            role=SubscriberRole.BIRTH_PARTNER,
        )


async def test_can_update_subscriber_contact_methods(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    assert subscription.contact_methods == []
    subscription = await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=["email"],
    )
    assert subscription.contact_methods == [ContactMethod.EMAIL]


async def test_can_update_subscriber_contact_methods_twice(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    assert subscription.contact_methods == []
    subscription = await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=["sms"],
    )
    assert subscription.contact_methods == [ContactMethod.SMS.value]
    subscription = await subscription_management_service.update_contact_methods(
        requester_id=SUBSCRIBER,
        subscription_id=subscription.id,
        contact_methods=["sms"],
    )
    assert subscription.contact_methods == [ContactMethod.SMS.value]


async def test_cannot_update_subscriber_contact_methods_with_invalid_value(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    with pytest.raises(SubscriptionContactMethodInvalid):
        await subscription_management_service.update_contact_methods(
            requester_id=SUBSCRIBER,
            subscription_id=subscription.id,
            contact_methods=["test"],
        )


async def test_only_subscriber_can_update_contact_methods(
    subscription_management_service: SubscriptionManagementService, subscription: SubscriptionDTO
) -> None:
    with pytest.raises(UnauthorizedSubscriptionUpdateRequest):
        await subscription_management_service.update_contact_methods(
            requester_id=BIRTHING_PERSON,
            subscription_id=subscription.id,
            contact_methods=["email"],
        )


async def test_invalid_id_raises_error_update_contact_methods(
    subscription_management_service: SubscriptionManagementService,
) -> None:
    with pytest.raises(SubscriptionIdInvalid):
        await subscription_management_service.update_contact_methods(
            requester_id=SUBSCRIBER,
            subscription_id="test",
            contact_methods=["email"],
        )


async def test_cannot_update_contact_methods_for_non_existent_subscription(
    subscription_management_service: SubscriptionManagementService,
) -> None:
    with pytest.raises(SubscriptionNotFoundById):
        await subscription_management_service.update_contact_methods(
            requester_id=SUBSCRIBER,
            subscription_id=str(uuid4()),
            contact_methods=["sms"],
        )
