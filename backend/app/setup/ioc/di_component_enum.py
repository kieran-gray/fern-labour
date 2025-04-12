from enum import StrEnum


class ComponentEnum(StrEnum):
    DEFAULT = ""
    ADMIN = "admin"
    LABOUR = "labour"
    LABOUR_EVENTS = "labour_events"
    EVENTS = "events"
    USER = "user"
    INVITES = "invites"
    NOTIFICATIONS = "notifications"
    NOTIFICATION_EVENTS = "notification_events"
    NOTIFICATION_GENERATORS = "notification_generators"
    SUBSCRIPTIONS = "subscriptions"
    PAYMENTS = "payments"
    PAYMENT_EVENTS = "payment_events"

    def __repr__(self) -> str:
        return self.value
