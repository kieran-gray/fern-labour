from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from app.labour.application.security.token_generator import TokenGenerator
from app.labour.application.services.labour_invite_service import (
    LabourInviteService,
)
from app.labour.application.services.labour_service import LabourService
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.labour.domain.labour.exceptions import InvalidLabourId
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.subscription.application.services.subscription_service import SubscriptionService
from app.subscription.domain.exceptions import SubscriberAlreadySubscribed
from app.user.application.services.user_query_service import UserQueryService
from app.user.domain.entity import User
from app.user.domain.exceptions import UserNotFoundById
from app.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "test_birthing_person"
SUBSCRIBER = "test_subscriber"


@pytest_asyncio.fixture
async def labour_invite_service(
    user_service: UserQueryService,
    subscription_query_service: SubscriptionQueryService,
    token_generator: TokenGenerator,
) -> LabourInviteService:
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
    return LabourInviteService(
        user_service=user_service,
        event_producer=AsyncMock(),
        subscription_query_service=subscription_query_service,
        token_generator=token_generator,
    )


def has_sent_email(labour_invite_service: LabourInviteService) -> bool:
    return labour_invite_service._event_producer.publish.call_count > 0


async def test_can_send_invite(
    labour_service: LabourService,
    labour_invite_service: LabourInviteService,
) -> None:
    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    await labour_invite_service.send_invite(
        birthing_person_id=BIRTHING_PERSON, labour_id=labour.id, invite_email="test@email.com"
    )
    assert has_sent_email(labour_invite_service=labour_invite_service)


async def test_cannnot_send_invite_for_non_existent_birthing_person(
    labour_invite_service: LabourInviteService,
) -> None:
    with pytest.raises(UserNotFoundById):
        await labour_invite_service.send_invite(
            birthing_person_id="fake", labour_id=str(uuid4()), invite_email="test@email.com"
        )


async def test_cannnot_send_invite_for_invalid_labour_id(
    labour_invite_service: LabourInviteService,
) -> None:
    with pytest.raises(InvalidLabourId):
        await labour_invite_service.send_invite(
            birthing_person_id=BIRTHING_PERSON,
            labour_id="invalid",
            invite_email="test@email.com",
        )


async def test_cannnot_send_invite_for_email_already_subscribed(
    labour_invite_service: LabourInviteService,
    subscription_service: SubscriptionService,
    labour_service: LabourService,
) -> None:
    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    await labour_service.update_labour_payment_plan(
        birthing_person_id=BIRTHING_PERSON, payment_plan=LabourPaymentPlan.INNER_CIRCLE.value
    )
    token = labour_invite_service._token_generator.generate(labour.id)

    await subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )

    with pytest.raises(SubscriberAlreadySubscribed):
        await labour_invite_service.send_invite(
            birthing_person_id=BIRTHING_PERSON,
            labour_id=labour.id,
            invite_email="test@subscriber.com",
        )
