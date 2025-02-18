import logging
from uuid import UUID

from app.application.dtos.subscription import SubscriptionDTO
from app.application.events.producer import EventProducer
from app.application.security.token_generator import TokenGenerator
from app.application.services.get_labour_service import GetLabourService
from app.application.services.subscriber_service import SubscriberService
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.vo_labour_id import LabourId
from app.domain.services.subscribe_to import SubscribeToService
from app.domain.services.unsubscribe_from import UnsubscribeFromService
from app.domain.subscriber.exceptions import SubscriberCannotSubscribeToSelf
from app.domain.subscriber.vo_subscriber_id import SubscriberId
from app.domain.subscription.exceptions import (
    SubscriberNotSubscribed,
    SubscriptionTokenIncorrect,
    UnauthorizedSubscriptionRequest,
)
from app.domain.subscription.repository import SubscriptionRepository

log = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(
        self,
        get_labour_service: GetLabourService,
        subscriber_service: SubscriberService,
        subscription_repository: SubscriptionRepository,
        token_generator: TokenGenerator,
        event_producer: EventProducer,
    ):
        self._get_labour_service = get_labour_service
        self._subscriber_service = subscriber_service
        self._subscription_repository = subscription_repository
        self._token_generator = token_generator
        self._event_producer = event_producer

    async def get_subscriber_subscriptions(self, subscriber_id: str) -> list[SubscriptionDTO]:
        subscriber = await self._subscriber_service.get(subscriber_id=subscriber_id)
        subscriptions = await self._subscription_repository.filter(
            subscriber_id=SubscriberId(subscriber.id)
        )
        return [SubscriptionDTO.from_domain(subscription) for subscription in subscriptions]

    async def get_labour_subscriptions(
        self, requester_id: str, labour_id: str
    ) -> list[SubscriptionDTO]:
        labour = await self._get_labour_service.get_labour_by_id(labour_id=labour_id)
        if requester_id != labour.birthing_person_id:
            raise UnauthorizedSubscriptionRequest()

        subscriptions = await self._subscription_repository.filter(
            labour_id=LabourId(UUID(labour.id))
        )
        return [SubscriptionDTO.from_domain(subscription) for subscription in subscriptions]

    async def subscribe_to(self, subscriber_id: str, labour_id: str, token: str) -> SubscriptionDTO:
        subscriber = await self._subscriber_service.get(subscriber_id=subscriber_id)
        labour = await self._get_labour_service.get_labour_by_id(labour_id=labour_id)

        if labour.birthing_person_id == subscriber_id:
            raise SubscriberCannotSubscribeToSelf()

        if not self._token_generator.validate(labour.id, token):
            raise SubscriptionTokenIncorrect()

        labour_domain_id = LabourId(UUID(labour.id))
        birthing_person_domain_id = BirthingPersonId(labour.birthing_person_id)
        subscriber_domain_id = SubscriberId(subscriber.id)

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
        subscriber = await self._subscriber_service.get(subscriber_id=subscriber_id)

        labour_domain_id = LabourId(UUID(labour_id))
        subscriber_domain_id = SubscriberId(subscriber.id)

        subscription = await self._subscription_repository.filter_one_or_none(
            subscriber_id=subscriber_domain_id, labour_id=labour_domain_id
        )

        if not subscription:
            raise SubscriberNotSubscribed()

        subscription = UnsubscribeFromService().unsubscribe_from(subscription=subscription)

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)
