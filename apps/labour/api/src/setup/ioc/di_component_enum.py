from enum import StrEnum


class ComponentEnum(StrEnum):
    DEFAULT = ""
    LABOUR = "labour"
    LABOUR_EVENTS = "labour_events"
    EVENTS = "events"
    USER = "user"
    INVITES = "invites"
    SUBSCRIPTION = "subscription"
    SUBSCRIPTION_EVENTS = "subscription_events"
    PAYMENTS = "payments"

    def __repr__(self) -> str:
        return self.value
