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


class NotificationTemplate(StrEnum):
    LABOUR_UPDATE = "labour_update"
    LABOUR_INVITE = "labour_invite"
    SUBSCRIBER_INVITE = "subscriber_invite"
    CONTACT_US_SUBMISSION = "contact_us_submission"
