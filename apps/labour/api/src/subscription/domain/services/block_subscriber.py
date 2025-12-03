from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import SubscriberIsBlocked


class BlockSubscriberService:
    def block_subscriber(self, subscription: Subscription) -> Subscription:
        if subscription.status is SubscriptionStatus.BLOCKED:
            raise SubscriberIsBlocked()

        subscription.update_status(SubscriptionStatus.BLOCKED)

        return subscription
