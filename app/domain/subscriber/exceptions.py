from typing import Any

from app.domain.base.exceptions import DomainError


class SubscriberAlreadySubscribedToBirthingPerson(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber already subscribed to birthing person")


class SubscriberNotSubscribedToBirthingPerson(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber is not subscribed to birthing person")


class SubscriberNotFoundById(DomainError):
    def __init__(self, subscriber_id: Any) -> None:
        super().__init__(f"Subscriber with id '{subscriber_id}' is not found.")


class SubscriberExistsWithID(DomainError):
    def __init__(self, subscriber_id: Any) -> None:
        super().__init__(f"Subscriber with id '{subscriber_id}' already exists.")


class SubscriptionTokenIncorrect(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscription token is incorrect.")
