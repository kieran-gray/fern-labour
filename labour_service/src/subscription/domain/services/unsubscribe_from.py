from src.subscription.domain.entity import Subscription
from src.subscription.domain.enums import SubscriptionStatus
from src.subscription.domain.exceptions import SubscriberNotSubscribed


class UnsubscribeFromService:
    def unsubscribe_from(self, subscription: Subscription) -> Subscription:
        if subscription.status is not SubscriptionStatus.SUBSCRIBED:
            raise SubscriberNotSubscribed()

        subscription.update_status(SubscriptionStatus.UNSUBSCRIBED)

        return subscription
