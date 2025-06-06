import logging
from uuid import UUID

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.application.unit_of_work import UnitOfWork
from src.core.domain.domain_event.repository import DomainEventRepository
from src.labour.application.security.token_generator import TokenGenerator
from src.labour.application.services.labour_query_service import LabourQueryService
from src.labour.domain.labour.exceptions import (
    InvalidLabourId,
)
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.subscription.application.dtos import SubscriptionDTO
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import (
    SubscriberNotSubscribed,
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
    SubscriptionTokenIncorrect,
)
from src.subscription.domain.repository import SubscriptionRepository
from src.subscription.domain.services.subscribe_to import SubscribeToService
from src.subscription.domain.services.unsubscribe_from import UnsubscribeFromService
from src.subscription.domain.value_objects.subscription_id import SubscriptionId
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(
        self,
        labour_query_service: LabourQueryService,
        subscription_repository: SubscriptionRepository,
        domain_event_repository: DomainEventRepository,
        unit_of_work: UnitOfWork,
        token_generator: TokenGenerator,
        domain_event_publisher: DomainEventPublisher,
    ):
        self._labour_query_service = labour_query_service
        self._subscription_repository = subscription_repository
        self._domain_event_repository = domain_event_repository
        self._unit_of_work = unit_of_work
        self._token_generator = token_generator
        self._domain_event_publisher = domain_event_publisher

    async def subscribe_to(self, subscriber_id: str, labour_id: str, token: str) -> SubscriptionDTO:
        if not self._token_generator.validate(labour_id, token):
            raise SubscriptionTokenIncorrect()

        labour = await self._labour_query_service.get_labour_by_id(labour_id=labour_id)

        labour_domain_id = LabourId(UUID(labour_id))
        birthing_person_domain_id = UserId(labour.birthing_person_id)
        subscriber_domain_id = UserId(subscriber_id)

        await self._labour_query_service.can_accept_subscriber(
            subscriber_id=subscriber_id,
            labour_id=labour_id,
        )

        subscription = await self._subscription_repository.filter_one_or_none(
            subscriber_id=subscriber_domain_id, labour_id=labour_domain_id
        )
        if subscription:
            subscription = SubscribeToService().subscribe_to_from_existing_subscription(
                subscription=subscription
            )
        else:
            subscription = SubscribeToService().subscribe_to(
                labour_id=labour_domain_id,
                birthing_person_id=birthing_person_domain_id,
                subscriber_id=subscriber_domain_id,
            )

        async with self._unit_of_work:
            await self._subscription_repository.save(subscription)
            await self._domain_event_repository.save_many(subscription.clear_domain_events())

        self._domain_event_publisher.publish_batch_in_background()

        return SubscriptionDTO.from_domain(subscription)

    async def unsubscribe_from(self, subscriber_id: str, labour_id: str) -> SubscriptionDTO:
        try:
            labour_domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()

        subscriber_domain_id = UserId(subscriber_id)

        subscription = await self._subscription_repository.filter_one_or_none(
            subscriber_id=subscriber_domain_id, labour_id=labour_domain_id
        )

        if not subscription:
            raise SubscriberNotSubscribed()

        subscription = UnsubscribeFromService().unsubscribe_from(subscription=subscription)

        async with self._unit_of_work:
            await self._subscription_repository.save(subscription)
            await self._domain_event_repository.save_many(subscription.clear_domain_events())

        self._domain_event_publisher.publish_batch_in_background()

        return SubscriptionDTO.from_domain(subscription)

    async def ensure_can_update_access_level(self, subscription_id: str) -> None:
        try:
            subscription_domain_id = SubscriptionId(UUID(subscription_id))
        except ValueError:
            raise SubscriptionIdInvalid()
        subscription = await self._subscription_repository.get_by_id(
            subscription_id=subscription_domain_id
        )
        if not subscription:
            raise SubscriptionNotFoundById(subscription_id=subscription_id)

        if subscription.status != SubscriptionStatus.SUBSCRIBED:
            raise SubscriberNotSubscribed()

        return await self._labour_query_service.ensure_labour_is_active(
            labour_id=str(subscription.labour_id.value)
        )
