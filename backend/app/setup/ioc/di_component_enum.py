from enum import StrEnum


class ComponentEnum(StrEnum):
    DEFAULT = ""
    ADMIN = "admin"
    LABOUR = "labour"
    EVENTS = "events"
    USER = "user"
    NOTIFICATIONS = "notifications"
    SUBSCRIPTIONS = "subscriptions"
    PAYMENTS = "payments"

    def __repr__(self) -> str:
        return self.value
