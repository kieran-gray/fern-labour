from typing import Any

from app.domain.base.exceptions import DomainError, DomainValidationError


class SubscriptionIdInvalid(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Subscription ID is invalid.")


class SubscriberRoleInvalid(DomainValidationError):
    def __init__(self, role: str) -> None:
        super().__init__(f"Subscriber role '{role}' is invalid.")


class SubscriptionContactMethodInvalid(DomainValidationError):
    def __init__(self, contact_method: str) -> None:
        super().__init__(f"Contact method '{contact_method}' is invalid.")


class SubscriberAlreadySubscribed(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber already subscribed to labour.")


class SubscriberNotSubscribed(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber is not subscribed to labour.")


class SubscriberIsBlocked(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscriber cannot subscribe to labour, blocked.")


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


class MaximumNumberOfSubscribersReached(DomainError):
    def __init__(self) -> None:
        super().__init__(
            "Maximum number of subscribers reached for plan. Upgrade for more subscribers."
        )
