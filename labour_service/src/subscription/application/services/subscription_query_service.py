import logging
from uuid import UUID

from src.labour.domain.labour.exceptions import (
    InvalidLabourId,
)
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.subscription.application.dtos.subscription import SubscriptionDTO
from src.subscription.application.security.subscription_authorization_service import (
    SubscriptionAuthorizationService,
)
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import (
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
)
from src.subscription.domain.repository import SubscriptionRepository
from src.subscription.domain.value_objects.subscription_id import SubscriptionId
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class SubscriptionQueryService:
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        subscription_authorization_service: SubscriptionAuthorizationService,
    ):
        self._subscription_repository = subscription_repository
        self._subscription_authorization_service = subscription_authorization_service

    async def get_by_id(self, requester_id: str, subscription_id: str) -> SubscriptionDTO:
        try:
            subscription_domain_id = SubscriptionId(UUID(subscription_id))
        except ValueError:
            raise SubscriptionIdInvalid()

        subscription = await self._subscription_repository.get_by_id(
            subscription_id=subscription_domain_id
        )
        if not subscription:
            raise SubscriptionNotFoundById(subscription_id=subscription_id)

        await self._subscription_authorization_service.ensure_can_view_subscription(
            requester_id=requester_id, subscription=subscription
        )

        return SubscriptionDTO.from_domain(subscription)

    async def get_subscriber_subscriptions(self, subscriber_id: str) -> list[SubscriptionDTO]:
        subscriptions = await self._subscription_repository.filter(
            subscriber_id=UserId(subscriber_id), subscription_status=SubscriptionStatus.SUBSCRIBED
        )
        return [SubscriptionDTO.from_domain(subscription) for subscription in subscriptions]

    async def get_labour_subscriptions(
        self, requester_id: str, labour_id: str
    ) -> list[SubscriptionDTO]:
        try:
            labour_domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()
        subscriptions = await self._subscription_repository.filter(
            labour_id=labour_domain_id, birthing_person_id=UserId(requester_id)
        )
        return [SubscriptionDTO.from_domain(subscription) for subscription in subscriptions]
