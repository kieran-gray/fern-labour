from dataclasses import dataclass
from typing import Self

from app.domain.base.aggregate_root import AggregateRoot
from app.domain.subscriber.vo_subscriber_id import SubscriberId


@dataclass(eq=False, kw_only=True)
class Subscriber(AggregateRoot[SubscriberId]):
    first_name: str
    last_name: str
    phone_number: str | None = None
    email: str | None = None

    @classmethod
    def create(
        cls,
        *,
        id: str,
        first_name: str,
        last_name: str,
        phone_number: str | None = None,
        email: str | None = None,
    ) -> Self:
        return cls(
            id_=SubscriberId(id),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
        )
