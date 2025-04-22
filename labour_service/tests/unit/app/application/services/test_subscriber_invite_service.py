from unittest.mock import AsyncMock

import pytest_asyncio

from src.subscription.application.services.subscriber_invite_service import SubscriberInviteService
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "test_birthing_person"
SUBSCRIBER = "test_subscriber"


@pytest_asyncio.fixture
async def subscriber_invite_service(user_service: UserQueryService) -> SubscriberInviteService:
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
    return SubscriberInviteService(user_service=user_service, event_producer=AsyncMock())


def has_sent_email(subscriber_invite_service: SubscriberInviteService) -> bool:
    return subscriber_invite_service._event_producer.publish.call_count > 0


async def test_can_send_invite(
    subscriber_invite_service: SubscriberInviteService,
) -> None:
    await subscriber_invite_service.send_invite(
        subscriber_id=SUBSCRIBER, invite_email="test@email.com"
    )
    assert has_sent_email(subscriber_invite_service=subscriber_invite_service)
