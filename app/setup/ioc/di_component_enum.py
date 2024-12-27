from enum import StrEnum


class ComponentEnum(StrEnum):
    DEFAULT = ""
    LABOUR = "labour"
    EVENTS = "events"
    SUBSCRIBER = "subscriber"

    def __repr__(self) -> str:
        return self.value
