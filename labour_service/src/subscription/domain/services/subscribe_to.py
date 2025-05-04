from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import (
    SubscriberAlreadyRequested,
    SubscriberAlreadySubscribed,
    SubscriberIsBlocked,
)
from src.user.domain.value_objects.user_id import UserId


class SubscribeToService:
    """Subscribers begin on REQUESTED status and transition to SUBSCRIBED when approved."""

    def subscribe_to(
        self,
        labour_id: LabourId,
        birthing_person_id: UserId,
        subscriber_id: UserId,
    ) -> Subscription:
        return Subscription.create(
            labour_id=labour_id,
            birthing_person_id=birthing_person_id,
            subscriber_id=subscriber_id,
        )

    def subscribe_to_from_existing_subscription(self, subscription: Subscription) -> Subscription:
        if subscription.status is SubscriptionStatus.BLOCKED:
            raise SubscriberIsBlocked()

        if subscription.status is SubscriptionStatus.SUBSCRIBED:
            raise SubscriberAlreadySubscribed()

        if subscription.status is SubscriptionStatus.REQUESTED:
            raise SubscriberAlreadyRequested()

        subscription.request()

        return subscription
