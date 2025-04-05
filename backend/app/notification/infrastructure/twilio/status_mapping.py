from app.notification.domain.enums import NotificationStatus

TWILIO_STATUS_MAPPING = {
    "accepted": NotificationStatus.SENT.value,
    "queued": NotificationStatus.SENT.value,
    "sent": NotificationStatus.SENT.value,
    "delivered": NotificationStatus.SUCCESS.value,
    "read": NotificationStatus.SUCCESS.value,
    "undelivered": NotificationStatus.FAILURE.value,
    "failed": NotificationStatus.FAILURE.value,
}
