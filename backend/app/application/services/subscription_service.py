import logging
from uuid import UUID

from app.application.dtos.subscription import SubscriptionDTO
from app.application.events.producer import EventProducer
from app.application.security.token_generator import TokenGenerator
from app.application.services.user_service import UserService
from app.domain.user.exceptions import UserCannotSubscribeToSelf
from app.domain.user.vo_user_id import UserId
from app.labour.application.services.get_labour_service import GetLabourService
from app.labour.domain.labour.enums import LabourPaymentPlan
from app.labour.domain.labour.exceptions import (
    InsufficientLabourPaymentPlan,
    InvalidLabourId,
    UnauthorizedLabourRequest,
)
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.domain.subscription.constants import INNER_CIRCLE_MAX_SUBSCRIBERS
from app.labour.domain.subscription.enums import SubscriptionStatus
from app.labour.domain.subscription.exceptions import (
    MaximumNumberOfSubscribersReached,
    SubscriberNotSubscribed,
    SubscriptionIdInvalid,
    SubscriptionNotFoundById,
    SubscriptionTokenIncorrect,
    UnauthorizedSubscriptionRequest,
)
from app.labour.domain.subscription.repository import SubscriptionRepository
from app.labour.domain.subscription.services.subscribe_to import SubscribeToService
from app.labour.domain.subscription.services.unsubscribe_from import UnsubscribeFromService
from app.labour.domain.subscription.value_objects.subscription_id import SubscriptionId

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

        if (
            subscription.subscriber_id.value == requester_id
            and subscription.status is not SubscriptionStatus.SUBSCRIBED
        ):
            raise UnauthorizedSubscriptionRequest()

        return SubscriptionDTO.from_domain(subscription)

    async def get_subscriber_subscriptions(self, subscriber_id: str) -> list[SubscriptionDTO]:
        subscriber = await self._user_service.get(user_id=subscriber_id)
        subscriptions = await self._subscription_repository.filter(
            subscriber_id=UserId(subscriber.id), subscription_status=SubscriptionStatus.SUBSCRIBED
        )
        return [SubscriptionDTO.from_domain(subscription) for subscription in subscriptions]

    async def get_labour_subscriptions(
        self, requester_id: str, labour_id: str
    ) -> list[SubscriptionDTO]:
        labour = await self._get_labour_service.get_labour_by_id(labour_id=labour_id)
        if requester_id != labour.birthing_person_id:
            raise UnauthorizedSubscriptionRequest()

        labour_domain_id = LabourId(UUID(labour_id))
        subscriptions = await self._subscription_repository.filter(labour_id=labour_domain_id)
        return [SubscriptionDTO.from_domain(subscription) for subscription in subscriptions]

    async def subscribe_to(self, subscriber_id: str, labour_id: str, token: str) -> SubscriptionDTO:
        subscriber = await self._user_service.get(user_id=subscriber_id)
        labour = await self._get_labour_service.get_labour_by_id(labour_id=labour_id)

        if labour.birthing_person_id == subscriber_id:
            raise UserCannotSubscribeToSelf()

        if not self._token_generator.validate(labour.id, token):
            raise SubscriptionTokenIncorrect()

        labour_domain_id = LabourId(UUID(labour_id))
        birthing_person_domain_id = UserId(labour.birthing_person_id)
        subscriber_domain_id = UserId(subscriber.id)

        if not labour.payment_plan or labour.payment_plan == LabourPaymentPlan.SOLO.value:
            raise InsufficientLabourPaymentPlan()

        if labour.payment_plan == LabourPaymentPlan.INNER_CIRCLE.value:
            active_subscriptions = await self._subscription_repository.filter(
                labour_id=labour_domain_id, subscription_status=SubscriptionStatus.SUBSCRIBED
            )
            if len(active_subscriptions) >= INNER_CIRCLE_MAX_SUBSCRIBERS:
                raise MaximumNumberOfSubscribersReached()

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

        try:
            labour_domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()

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

    async def can_user_access_labour(self, requester_id: str, labour_id: str) -> bool:
        user = await self._user_service.get(user_id=requester_id)

        try:
            labour_domain_id = LabourId(UUID(labour_id))
        except ValueError:
            raise InvalidLabourId()

        user_domain_id = UserId(user.id)

        labour = await self._get_labour_service.get_labour_by_id(labour_id=labour_id)
        if labour.birthing_person_id == requester_id:
            return True

        subscriptions = await self._subscription_repository.filter(labour_id=labour_domain_id)

        for subscription in subscriptions:
            if (
                subscription.subscriber_id == user_domain_id
                and subscription.status == SubscriptionStatus.SUBSCRIBED
            ):
                return True
        raise UnauthorizedLabourRequest()
