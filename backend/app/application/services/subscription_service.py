import logging
from uuid import UUID

from app.application.dtos.subscription import SubscriptionDTO
from app.application.events.producer import EventProducer
from app.application.security.token_generator import TokenGenerator
from app.application.services.get_labour_service import GetLabourService
from app.application.services.user_service import UserService
from app.domain.labour.vo_labour_id import LabourId
from app.domain.services.subscribe_to import SubscribeToService
from app.domain.services.unsubscribe_from import UnsubscribeFromService
from app.domain.subscription.exceptions import (
    SubscriberNotSubscribed,
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
    SubscriptionTokenIncorrect,
    UnauthorizedSubscriptionRequest,
)
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.vo_subscription_id import SubscriptionId
from app.domain.user.exceptions import UserCannotSubscribeToSelf
from app.domain.user.vo_user_id import UserId

log = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(
        self,
        get_labour_service: GetLabourService,
        user_service: UserService,
        subscription_repository: SubscriptionRepository,
        token_generator: TokenGenerator,
        event_producer: EventProducer,
    ):
        self._get_labour_service = get_labour_service
        self._user_service = user_service
        self._subscription_repository = subscription_repository
        self._token_generator = token_generator
        self._event_producer = event_producer

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

        if (
            subscription.subscriber_id.value != requester_id
            and subscription.birthing_person_id.value != requester_id
        ):
            raise UnauthorizedSubscriptionRequest()

        return SubscriptionDTO.from_domain(subscription)

    async def get_subscriber_subscriptions(self, subscriber_id: str) -> list[SubscriptionDTO]:
        # Getting the subscriber ensures that one exists, and handles throwing accurate error if not
        subscriber = await self._user_service.get(user_id=subscriber_id)
        subscriptions = await self._subscription_repository.filter(
            subscriber_id=UserId(subscriber.id)
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
        subscriber = await self._user_service.get(user_id=subscriber_id)
        labour = await self._get_labour_service.get_labour_by_id(labour_id=labour_id)

        if labour.birthing_person_id == subscriber_id:
            raise UserCannotSubscribeToSelf()

        if not self._token_generator.validate(labour.id, token):
            raise SubscriptionTokenIncorrect()

        labour_domain_id = LabourId(UUID(labour.id))
        birthing_person_domain_id = UserId(labour.birthing_person_id)
        subscriber_domain_id = UserId(subscriber.id)

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
        subscriber = await self._user_service.get(user_id=subscriber_id)

        labour_domain_id = LabourId(UUID(labour_id))
        subscriber_domain_id = UserId(subscriber.id)

        subscription = await self._subscription_repository.filter_one_or_none(
            subscriber_id=subscriber_domain_id, labour_id=labour_domain_id
        )

        if not subscription:
            raise SubscriberNotSubscribed()

        subscription = UnsubscribeFromService().unsubscribe_from(subscription=subscription)

        await self._subscription_repository.save(subscription)

        await self._event_producer.publish_batch(subscription.clear_domain_events())

        return SubscriptionDTO.from_domain(subscription)
