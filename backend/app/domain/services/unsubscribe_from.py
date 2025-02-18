from app.domain.subscription.entity import Subscription
from app.domain.subscription.enums import SubscriptionStatus
from app.domain.subscription.exceptions import SubscriberNotSubscribed


class UnsubscribeFromService:
    def unsubscribe_from(self, subscription: Subscription) -> Subscription:
        if subscription.status is not SubscriptionStatus.SUBSCRIBED:
            raise SubscriberNotSubscribed()

        subscription.update_status(SubscriptionStatus.UNSUBSCRIBED)

        return subscription
