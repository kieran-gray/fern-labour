from typing import Any

from app.domain.base.exceptions import DomainError


class SubscriberCannotSubscribeToSelf(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot subscribe to self")


class SubscriberNotFoundById(DomainError):
    def __init__(self, subscriber_id: Any) -> None:
        super().__init__(f"Subscriber with id '{subscriber_id}' is not found.")


class SubscriberExistsWithID(DomainError):
    def __init__(self, subscriber_id: Any) -> None:
        super().__init__(f"Subscriber with id '{subscriber_id}' already exists.")
