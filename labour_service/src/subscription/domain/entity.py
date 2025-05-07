from dataclasses import dataclass, field
from typing import Self
from uuid import UUID, uuid4

from fern_labour_core.aggregate_root import AggregateRoot

from src.labour.domain.labour.value_objects.labour_id import LabourId
from src.subscription.domain.enums import (
    ContactMethod,
    SubscriberRole,
    SubscriptionAccessLevel,
    SubscriptionStatus,
)
from src.subscription.domain.events import SubscriberApproved, SubscriberRequested
from src.subscription.domain.value_objects.subscription_id import SubscriptionId
from src.user.domain.value_objects.user_id import UserId


@dataclass(eq=False, kw_only=True)
class Subscription(AggregateRoot[SubscriptionId]):
    labour_id: LabourId
    birthing_person_id: UserId
    subscriber_id: UserId
    role: SubscriberRole
    status: SubscriptionStatus
    access_level: SubscriptionAccessLevel
    contact_methods: list[ContactMethod] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        labour_id: LabourId,
        birthing_person_id: UserId,
        subscriber_id: UserId,
        status: SubscriptionStatus = SubscriptionStatus.REQUESTED,
        role: SubscriberRole = SubscriberRole.FRIENDS_AND_FAMILY,
        access_level: SubscriptionAccessLevel = SubscriptionAccessLevel.BASIC,
        contact_methods: list[ContactMethod] | None = None,
        subscription_id: UUID | None = None,
    ) -> Self:
        subscription_id = subscription_id or uuid4()
        subscription = cls(
            id_=SubscriptionId(subscription_id),
            labour_id=labour_id,
            birthing_person_id=birthing_person_id,
            subscriber_id=subscriber_id,
            role=role,
            status=status,
            access_level=access_level,
            contact_methods=contact_methods or [],
        )
        subscription.add_domain_event(
            SubscriberRequested.create(
                data={
                    "labour_id": str(labour_id.value),
                    "birthing_person_id": birthing_person_id.value,
                    "subscriber_id": subscriber_id.value,
                    "subscription_id": str(subscription.id_),
                }
            )
        )
        return subscription

    def request(self) -> None:
        self.add_domain_event(
            SubscriberRequested.create(
                data={
                    "labour_id": str(self.labour_id.value),
                    "birthing_person_id": self.birthing_person_id.value,
                    "subscriber_id": self.subscriber_id.value,
                    "subscription_id": str(self.id_),
                }
            )
        )
        self.status = SubscriptionStatus.REQUESTED

    def approve(self) -> None:
        self.add_domain_event(
            SubscriberApproved.create(
                data={
                    "labour_id": str(self.labour_id.value),
                    "birthing_person_id": self.birthing_person_id.value,
                    "subscriber_id": self.subscriber_id.value,
                    "subscription_id": str(self.id_),
                }
            )
        )
        self.status = SubscriptionStatus.SUBSCRIBED

    def update_role(self, role: SubscriberRole) -> None:
        self.role = role

    def update_status(self, status: SubscriptionStatus) -> None:
        self.status = status

    def update_access_level(self, access_level: SubscriptionAccessLevel) -> None:
        self.access_level = access_level

    def update_contact_methods(self, contact_methods: list[ContactMethod]) -> None:
        self.contact_methods = contact_methods
