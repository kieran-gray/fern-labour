from enum import StrEnum


class NotificationStatus(StrEnum):
    CREATED = "created"
    SENT = "sent"
    FAILURE = "failure"
    SUCCESS = "success"
