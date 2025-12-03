from typing import Any

from fern_labour_core.exceptions.domain import DomainError, DomainValidationError


class SubscriptionIdInvalid(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Subscription ID is invalid.")


class SubscriberRoleInvalid(DomainValidationError):
    def __init__(self, role: str) -> None:
        super().__init__(f"Subscriber role '{role}' is invalid.")


class SubscriptionContactMethodInvalid(DomainValidationError):
    def __init__(self, contact_method: str) -> None:
        super().__init__(f"Contact method '{contact_method}' is invalid.")


class SubscriptionAccessLevelInvalid(DomainValidationError):
    def __init__(self, access_level: str) -> None:
        super().__init__(f"Subscription Access Level '{access_level}' is invalid.")


class SubscriberAlreadySubscribed(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber already subscribed to labour.")


class SubscriberAlreadyRequested(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber already requested access to labour.")


class SubscriberNotSubscribed(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber is not subscribed to labour.")


class SubscriberIsBlocked(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber is blocked.")


class SubscriberIsNotBlocked(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber is not blocked.")


class SubscriberIsRemoved(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber is removed.")


class SubscriptionTokenIncorrect(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscription token is incorrect.")


class SubscriptionNotFoundById(DomainError):
    def __init__(self, subscription_id: Any) -> None:
        super().__init__(f"Subscription with ID '{subscription_id}' not found.")


class UnauthorizedSubscriptionUpdateRequest(DomainError):
    def __init__(self) -> None:
        super().__init__("User is not authorized to make requested changes to subscription.")


class UnauthorizedSubscriptionRequest(DomainError):
    def __init__(self) -> None:
        super().__init__("User is not authorized to access requested subscriptions.")
