from app.domain.labour.vo_labour_id import LabourId
from app.domain.subscription.entity import Subscription
from app.domain.subscription.enums import SubscriptionStatus
from app.domain.subscription.exceptions import SubscriberAlreadySubscribed, SubscriberIsBlocked
from app.domain.user.vo_user_id import UserId


class SubscribeToService:
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

        subscription.update_status(SubscriptionStatus.SUBSCRIBED)

        return subscription
