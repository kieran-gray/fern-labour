from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import (
    SubscriberAlreadySubscribed,
    SubscriberIsBlocked,
)


class ApproveSubscriberService:
    def approve_subscriber(self, subscription: Subscription) -> Subscription:
        if subscription.status is SubscriptionStatus.BLOCKED:
            raise SubscriberIsBlocked()

        if subscription.status is SubscriptionStatus.SUBSCRIBED:
            raise SubscriberAlreadySubscribed()

        subscription.approve()

        return subscription
