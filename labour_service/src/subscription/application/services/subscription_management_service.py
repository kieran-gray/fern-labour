import logging
from uuid import UUID

from fern_labour_core.events.producer import EventProducer

from src.subscription.application.dtos.subscription import SubscriptionDTO
from src.subscription.application.security.subscription_authorization_service import (
    SubscriptionAuthorizationService,
)
from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import ContactMethod, SubscriberRole
from src.subscription.domain.exceptions import (
    SubscriberRoleInvalid,
    SubscriptionContactMethodInvalid,
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
)
from src.subscription.domain.repository import SubscriptionRepository
from src.subscription.domain.services.approve_subscriber import ApproveSubscriberService
from src.subscription.domain.services.block_subscriber import BlockSubscriberService
from src.subscription.domain.services.remove_subscriber import RemoveSubscriberService
from src.subscription.domain.services.unblock_subscriber import UnblockSubscriberService
from src.subscription.domain.services.update_contact_methods import (
    UpdateContactMethodsService,
)
from src.subscription.domain.value_objects.subscription_id import SubscriptionId

log = logging.getLogger(__name__)


class SubscriptionManagementService:
    def __init__(
        self,
        subscription_repository: SubscriptionRepository,
        subscription_authorization_service: SubscriptionAuthorizationService,
        event_producer: EventProducer,
    ):
        self._subscription_repository = subscription_repository
        self._subscription_authorization_service = subscription_authorization_service
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

    async def approve_subscriber(self, requester_id: str, subscription_id: str) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        await self._subscription_authorization_service.ensure_can_manage_as_birthing_person(
            requester_id=requester_id, subscription=subscription
        )

        subscription = ApproveSubscriberService().approve_subscriber(subscription=subscription)

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)

    async def remove_subscriber(self, requester_id: str, subscription_id: str) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        await self._subscription_authorization_service.ensure_can_manage_as_birthing_person(
            requester_id=requester_id, subscription=subscription
        )

        subscription = RemoveSubscriberService().remove_subscriber(subscription=subscription)

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)

    async def block_subscriber(self, requester_id: str, subscription_id: str) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        await self._subscription_authorization_service.ensure_can_manage_as_birthing_person(
            requester_id=requester_id, subscription=subscription
        )

        subscription = BlockSubscriberService().block_subscriber(subscription=subscription)

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)

    async def unblock_subscriber(self, requester_id: str, subscription_id: str) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        await self._subscription_authorization_service.ensure_can_manage_as_birthing_person(
            requester_id=requester_id, subscription=subscription
        )

        subscription = UnblockSubscriberService().unblock_subscriber(subscription=subscription)

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)

    async def update_role(
        self, requester_id: str, subscription_id: str, role: str
    ) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        await self._subscription_authorization_service.ensure_can_manage_as_birthing_person(
            requester_id=requester_id, subscription=subscription
        )

        try:
            new_role = SubscriberRole(role)
        except ValueError:
            raise SubscriberRoleInvalid(role=role)

        subscription.update_role(new_role)

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)

    async def update_contact_methods(
        self, requester_id: str, subscription_id: str, contact_methods: list[str]
    ) -> SubscriptionDTO:
        subscription = await self._get_subscription(subscription_id=subscription_id)

        await self._subscription_authorization_service.ensure_can_manage_as_subscriber(
            requester_id=requester_id, subscription=subscription
        )

        new_contact_methods = []
        for contact_method in contact_methods:
            try:
                new_contact_methods.append(ContactMethod(contact_method))
            except ValueError:
                raise SubscriptionContactMethodInvalid(contact_method=contact_method)

        subscription = UpdateContactMethodsService().update_contact_methods(
            subscription=subscription, contact_methods=new_contact_methods
        )

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)
