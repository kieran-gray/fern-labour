from app.subscription.domain.entity import Subscription
from app.subscription.domain.enums import SubscriptionStatus
from app.subscription.domain.exceptions import SubscriberNotSubscribed


class UnsubscribeFromService:
    def unsubscribe_from(self, subscription: Subscription) -> Subscription:
        if subscription.status is not SubscriptionStatus.SUBSCRIBED:
            raise SubscriberNotSubscribed()

        subscription.update_status(SubscriptionStatus.UNSUBSCRIBED)

        return subscription
