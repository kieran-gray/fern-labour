from enum import StrEnum


class NotificationChannel(StrEnum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"


class NotificationStatus(StrEnum):
    CREATED = "created"
    SENT = "sent"
    FAILURE = "failure"
    SUCCESS = "success"
