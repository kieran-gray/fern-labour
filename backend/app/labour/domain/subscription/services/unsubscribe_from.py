from app.labour.domain.subscription.entity import Subscription
from app.labour.domain.subscription.enums import SubscriptionStatus
from app.labour.domain.subscription.exceptions import SubscriberNotSubscribed


class UnsubscribeFromService:
    def unsubscribe_from(self, subscription: Subscription) -> Subscription:
        if subscription.status is not SubscriptionStatus.SUBSCRIBED:
            raise SubscriberNotSubscribed()

        subscription.update_status(SubscriptionStatus.UNSUBSCRIBED)

        return subscription
