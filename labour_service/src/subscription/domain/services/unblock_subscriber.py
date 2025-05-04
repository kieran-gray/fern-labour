from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import SubscriberIsNotBlocked


class UnblockSubscriberService:
    def unblock_subscriber(self, subscription: Subscription) -> Subscription:
        if subscription.status is not SubscriptionStatus.BLOCKED:
            raise SubscriberIsNotBlocked()

        subscription.update_status(SubscriptionStatus.REMOVED)

        return subscription
