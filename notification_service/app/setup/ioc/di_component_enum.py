from enum import StrEnum


class ComponentEnum(StrEnum):
    DEFAULT = ""
    EVENTS = "events"
    USER = "user"
    NOTIFICATIONS = "notifications"
    NOTIFICATION_EVENTS = "notification_events"
    NOTIFICATION_GENERATORS = "notification_generators"

    def __repr__(self) -> str:
        return self.value
