import pytest_asyncio

from app.notification.application.services.notification_service import NotificationService
from app.subscription.application.services.subscriber_invite_service import SubscriberInviteService
from app.user.application.services.user_service import UserService
from app.user.domain.entity import User
from app.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "test_birthing_person"
SUBSCRIBER = "test_subscriber"


@pytest_asyncio.fixture
async def subscriber_invite_service(
    user_service: UserService,
    notification_service: NotificationService,
) -> SubscriberInviteService:
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
    return SubscriberInviteService(
        user_service=user_service,
        notification_service=notification_service,
    )


async def test_can_send_invite(
    subscriber_invite_service: SubscriberInviteService,
) -> None:
    notification_service = subscriber_invite_service._notification_service

    assert await notification_service._notification_repository.filter() == []

    await subscriber_invite_service.send_invite(
        subscriber_id=SUBSCRIBER, invite_email="test@email.com"
    )
    assert await notification_service._notification_repository.filter() != []
