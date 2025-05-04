from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import SubscriberIsBlocked, SubscriberIsRemoved


class RemoveSubscriberService:
    def remove_subscriber(self, subscription: Subscription) -> Subscription:
        if subscription.status is SubscriptionStatus.BLOCKED:
            raise SubscriberIsBlocked()

        if subscription.status is SubscriptionStatus.REMOVED:
            raise SubscriberIsRemoved()

        subscription.update_status(SubscriptionStatus.REMOVED)

        return subscription
