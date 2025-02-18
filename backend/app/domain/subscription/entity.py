from dataclasses import dataclass, field
from typing import Self
from uuid import UUID, uuid4

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.labour.vo_labour_id import LabourId
from app.domain.subscriber.vo_subscriber_id import SubscriberId
from app.domain.subscription.enums import ContactMethod, SubscriberRole, SubscriptionStatus
from app.domain.subscription.vo_subscription_id import SubscriptionId


@dataclass(eq=False, kw_only=True)
class Subscription(AggregateRoot[SubscriptionId]):
    labour_id: LabourId
    birthing_person_id: BirthingPersonId
    subscriber_id: SubscriberId
    role: SubscriberRole
    status: SubscriptionStatus
    contact_methods: list[ContactMethod] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        labour_id: LabourId,
        birthing_person_id: BirthingPersonId,
        subscriber_id: SubscriberId,
        status: SubscriptionStatus = SubscriptionStatus.SUBSCRIBED,
        role: SubscriberRole = SubscriberRole.FRIENDS_AND_FAMILY,
        contact_methods: list[ContactMethod] | None = None,
        subscription_id: UUID | None = None,
    ) -> Self:
        subscription_id = subscription_id or uuid4()
        return cls(
            id_=SubscriptionId(subscription_id),
            labour_id=labour_id,
            birthing_person_id=birthing_person_id,
            subscriber_id=subscriber_id,
            role=role,
            contact_methods=contact_methods or [],
            status=status,
        )

    def update_role(self, role: SubscriberRole) -> None:
        self.role = role

    def update_status(self, status: SubscriptionStatus) -> None:
        self.status = status

    def update_contact_methods(self, contact_methods: list[ContactMethod]) -> None:
        self.contact_methods = contact_methods
