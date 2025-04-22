from dataclasses import dataclass, field
from typing import Self
from uuid import UUID, uuid4

from src.common.domain.aggregate_root import AggregateRoot
from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.subscription.domain.enums import ContactMethod, SubscriberRole, SubscriptionStatus
from src.subscription.domain.value_objects.subscription_id import SubscriptionId
from src.user.domain.value_objects.user_id import UserId


@dataclass(eq=False, kw_only=True)
class Subscription(AggregateRoot[SubscriptionId]):
    labour_id: LabourId
    birthing_person_id: UserId
    subscriber_id: UserId
    role: SubscriberRole
    status: SubscriptionStatus
    contact_methods: list[ContactMethod] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        labour_id: LabourId,
        birthing_person_id: UserId,
        subscriber_id: UserId,
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
