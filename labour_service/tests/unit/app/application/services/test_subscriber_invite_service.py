from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from src.core.infrastructure.security.rate_limiting.interface import RateLimiter
from src.subscription.application.exceptions import SubscriberInviteRateLimitExceeded
from src.subscription.application.services.subscriber_invite_service import SubscriberInviteService
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.value_objects.user_id import UserId

BIRTHING_PERSON = "test_birthing_person"
SUBSCRIBER = "test_subscriber"
RATE_LIMIT = 2


@pytest_asyncio.fixture
async def subscriber_invite_service(
    user_service: UserQueryService, rate_limiter: RateLimiter
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
        event_producer=AsyncMock(),
        rate_limiter=rate_limiter,
        rate_limit=RATE_LIMIT,
        rate_limit_expiry=60,
    )


def has_sent_email(subscriber_invite_service: SubscriberInviteService) -> bool:
    return subscriber_invite_service._event_producer.publish.call_count > 0


async def test_can_send_invite(
    subscriber_invite_service: SubscriberInviteService,
) -> None:
    await subscriber_invite_service.send_invite(
        subscriber_id=SUBSCRIBER, invite_email="test@email.com"
    )
    assert has_sent_email(subscriber_invite_service=subscriber_invite_service)


async def test_error_raised_after_exceeding_rate_limit(
    subscriber_invite_service: SubscriberInviteService,
) -> None:
    for _ in range(RATE_LIMIT):
        await subscriber_invite_service.send_invite(
            subscriber_id=SUBSCRIBER, invite_email="test@email.com"
        )
    with pytest.raises(SubscriberInviteRateLimitExceeded):
        await subscriber_invite_service.send_invite(
            subscriber_id=SUBSCRIBER, invite_email="test@email.com"
        )
