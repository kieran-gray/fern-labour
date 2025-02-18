from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.vo_labour_id import LabourId
from app.domain.subscriber.vo_subscriber_id import SubscriberId
from app.domain.subscription.entity import Subscription
from app.domain.subscription.enums import SubscriptionStatus
from app.domain.subscription.exceptions import SubscriberAlreadySubscribed, SubscriberIsBlocked


class SubscribeToService:
    def subscribe_to(
        self,
        labour_id: LabourId,
        birthing_person_id: BirthingPersonId,
        subscriber_id: SubscriberId,
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
