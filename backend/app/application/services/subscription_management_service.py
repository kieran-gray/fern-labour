import logging
from uuid import UUID

from app.application.dtos.subscription import SubscriptionDTO
from app.application.events.producer import EventProducer
from app.domain.subscription.entity import Subscription
from app.domain.subscription.enums import ContactMethod, SubscriberRole, SubscriptionStatus
from app.domain.subscription.exceptions import (
    SubscriberRoleInvalid,
    SubscriptionContactMethodInvalid,
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
    UnauthorizedSubscriptionUpdateRequest,
)
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.vo_subscription_id import SubscriptionId

log = logging.getLogger(__name__)


class SubscriptionManagementService:
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        event_producer: EventProducer,
    ):
        self._subscription_repository = subscription_repository
        self._event_producer = event_producer

    async def _get_subscription(self, subscription_id: str) -> Subscription:
        try:
            subscription_domain_id = SubscriptionId(UUID(subscription_id))
        except ValueError:
            raise SubscriptionIdInvalid()
        subscription = await self._subscription_repository.get_by_id(
            subscription_id=subscription_domain_id
        )
        if not subscription:
            raise SubscriptionNotFoundById(subscription_id=subscription_id)
        return subscription

    async def remove_subscriber(self, requester_id: str, subscription_id: str) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)
        if requester_id != subscription.birthing_person_id.value:
            raise UnauthorizedSubscriptionUpdateRequest()

        subscription.update_status(SubscriptionStatus.REMOVED)  # TODO maybe domain service

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)

    async def block_subscriber(self, requester_id: str, subscription_id: str) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        if requester_id != subscription.birthing_person_id.value:
            raise UnauthorizedSubscriptionUpdateRequest()

        subscription.update_status(SubscriptionStatus.BLOCKED)  # TODO maybe domain service

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)

    async def update_role(
        self, requester_id: str, subscription_id: str, role: str
    ) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        if requester_id != subscription.birthing_person_id.value:
            raise UnauthorizedSubscriptionUpdateRequest()

        try:
            new_role = SubscriberRole(role)
        except ValueError:
            raise SubscriberRoleInvalid(role=role)

        subscription.update_role(new_role)  # TODO maybe domain service

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)

    async def update_contact_methods(
        self, requester_id: str, subscription_id: str, contact_methods: list[str]
    ) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        if requester_id != subscription.subscriber_id.value:
            raise UnauthorizedSubscriptionUpdateRequest()

        new_contact_methods = []
        for contact_method in contact_methods:
            try:
                new_contact_methods.append(ContactMethod(contact_method))
            except ValueError:
                raise SubscriptionContactMethodInvalid(contact_method=contact_method)

        subscription.update_contact_methods(new_contact_methods)  # TODO maybe domain service

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)
