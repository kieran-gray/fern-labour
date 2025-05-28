from enum import StrEnum


class ComponentEnum(StrEnum):
    DEFAULT = ""
    EVENTS = "events"
    USER = "user"
    NOTIFICATIONS = "notifications"
    NOTIFICATION_EVENTS = "notification_events"

    def __repr__(self) -> str:
        return self.value
