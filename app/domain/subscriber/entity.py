from dataclasses import dataclass, field
from typing import Self

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.enums import ContactMethod
from app.domain.subscriber.events import SubscriberSubscribedTo, SubscriberUnsubscribedFrom
from app.domain.subscriber.exceptions import (
    SubscriberAlreadySubscribedToBirthingPerson,
    SubscriberNotSubscribedToBirthingPerson,
)
from app.domain.subscriber.vo_subscriber_id import SubscriberId


@dataclass(eq=False, kw_only=True)
class Subscriber(AggregateRoot[SubscriberId]):
    first_name: str
    last_name: str
    phone_number: str | None = None
    email: str | None = None
    contact_methods: list[ContactMethod] = field(default_factory=list)
    subscribed_to: list[BirthingPersonId] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        id: str,
        first_name: str,
        last_name: str,
        phone_number: str | None = None,
        email: str | None = None,
        contact_methods: list[str],
    ) -> Self:
        return cls(
            id_=SubscriberId(id),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            contact_methods=[ContactMethod(method) for method in contact_methods],
        )

    def subscribe_to(self, birthing_person_id: BirthingPersonId) -> None:
        if birthing_person_id in self.subscribed_to:
            raise SubscriberAlreadySubscribedToBirthingPerson()
        self.subscribed_to.append(birthing_person_id)
        self.add_domain_event(
            SubscriberSubscribedTo.create(
                data={
                    "subscriber_id": self.id_.value,
                    "birthing_person_id": birthing_person_id.value,
                }
            )
        )

    def unsubscribe_from(self, birthing_person_id: BirthingPersonId) -> None:
        if birthing_person_id not in self.subscribed_to:
            raise SubscriberNotSubscribedToBirthingPerson()
        self.subscribed_to.remove(birthing_person_id)
        self.add_domain_event(
            SubscriberUnsubscribedFrom.create(
                data={
                    "subscriber_id": self.id_.value,
                    "birthing_person_id": birthing_person_id.value,
                }
            )
        )
