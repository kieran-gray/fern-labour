from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.application.security.token_generator import TokenGenerator
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.labour_invite_service import (
    LabourInviteService,
)
from app.application.services.labour_service import LabourService
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_service import SubscriptionService
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.domain.labour.exceptions import LabourNotFoundById
from app.domain.subscription.exceptions import SubscriberAlreadySubscribed

BIRTHING_PERSON = "test_birthing_person"
SUBSCRIBER = "test_subscriber"


@pytest_asyncio.fixture
async def labour_invite_service(
    birthing_person_service: BirthingPersonService,
    notification_service: NotificationService,
    subscriber_service: SubscriberService,
    subscription_service: SubscriptionService,
    email_generation_service: EmailGenerationService,
    token_generator: TokenGenerator,
) -> LabourInviteService:
    await birthing_person_service.register(
        birthing_person_id=BIRTHING_PERSON,
        first_name="user",
        last_name="name",
    )
    await subscriber_service.register(
        subscriber_id=SUBSCRIBER,
        first_name="test",
        last_name="user",
        email="test@email.com",
    )
    return LabourInviteService(
        birthing_person_service=birthing_person_service,
        notification_service=notification_service,
        subscriber_service=subscriber_service,
        subscription_service=subscription_service,
        email_generation_service=email_generation_service,
        token_generator=token_generator,
    )


async def test_can_send_invite(
    labour_service: LabourService,
    labour_invite_service: LabourInviteService,
) -> None:
    notification_service = labour_invite_service._notification_service

    assert notification_service._email_notification_gateway.sent_notifications == []

    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    await labour_invite_service.send_invite(
        birthing_person_id=BIRTHING_PERSON, labour_id=labour.id, invite_email="test@email.com"
    )
    assert notification_service._email_notification_gateway.sent_notifications != []


async def test_cannnot_send_invite_for_non_existent_birthing_person(
    labour_invite_service: LabourInviteService,
) -> None:
    with pytest.raises(BirthingPersonNotFoundById):
        await labour_invite_service.send_invite(
            birthing_person_id="fake", labour_id=str(uuid4()), invite_email="test@email.com"
        )


async def test_cannnot_send_invite_for_non_existent_labour(
    labour_invite_service: LabourInviteService,
) -> None:
    with pytest.raises(LabourNotFoundById):
        await labour_invite_service.send_invite(
            birthing_person_id=BIRTHING_PERSON,
            labour_id=str(uuid4()),
            invite_email="test@email.com",
        )


async def test_cannnot_send_invite_for_email_already_subscribed(
    labour_invite_service: LabourInviteService,
    labour_service: LabourService,
) -> None:
    labour = await labour_service.plan_labour(
        birthing_person_id=BIRTHING_PERSON, first_labour=True, due_date=datetime.now(UTC)
    )
    token = labour_invite_service._token_generator.generate(labour.id)
    await labour_invite_service._subscription_service.subscribe_to(
        subscriber_id=SUBSCRIBER, labour_id=labour.id, token=token
    )

    with pytest.raises(SubscriberAlreadySubscribed):
        await labour_invite_service.send_invite(
            birthing_person_id=BIRTHING_PERSON, labour_id=labour.id, invite_email="test@email.com"
        )
