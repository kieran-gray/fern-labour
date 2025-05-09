from enum import StrEnum


class ComponentEnum(StrEnum):
    DEFAULT = ""
    EVENTS = "events"
    USER = "user"

    def __repr__(self) -> str:
        return self.value
