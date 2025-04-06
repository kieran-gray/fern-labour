import logging
from uuid import UUID

from app.common.infrastructure.events.interfaces.producer import EventProducer
from app.labour.application.security.token_generator import TokenGenerator
from app.labour.application.services.labour_query_service import LabourQueryService
from app.labour.domain.labour.exceptions import (
    InvalidLabourId,
)
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.subscription.application.dtos.subscription import SubscriptionDTO
from app.subscription.domain.enums import SubscriptionStatus
from app.subscription.domain.exceptions import (
    SubscriberNotSubscribed,
    SubscriptionTokenIncorrect,
)
from app.subscription.domain.repository import SubscriptionRepository
from app.subscription.domain.services.subscribe_to import SubscribeToService
from app.subscription.domain.services.unsubscribe_from import UnsubscribeFromService
from app.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(
        self,
        labour_query_service: LabourQueryService,
        subscription_repository: SubscriptionRepository,
        token_generator: TokenGenerator,
        event_producer: EventProducer,
    ):
        self._labour_query_service = labour_query_service
        self._subscription_repository = subscription_repository
        self._token_generator = token_generator
        self._event_producer = event_producer

    async def subscribe_to(self, subscriber_id: str, labour_id: str, token: str) -> SubscriptionDTO:
        if not self._token_generator.validate(labour_id, token):
            raise SubscriptionTokenIncorrect()

        labour = await self._labour_query_service.get_labour_by_id(labour_id=labour_id)

        labour_domain_id = LabourId(UUID(labour_id))
        birthing_person_domain_id = UserId(labour.birthing_person_id)
        subscriber_domain_id = UserId(subscriber_id)

        # TODO get a count from the DB instead
        active_subscriptions = await self._subscription_repository.filter(
            labour_id=labour_domain_id, subscription_status=SubscriptionStatus.SUBSCRIBED
        )

        await self._labour_query_service.can_accept_subscriber(
            subscriber_id=subscriber_id,
            labour_id=labour_id,
            current_active_subscriptions=len(active_subscriptions),
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

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

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

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)
