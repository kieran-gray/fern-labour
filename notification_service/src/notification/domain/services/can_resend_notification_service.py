from src.notification.domain.entity import Notification
from src.notification.domain.enums import NotificationStatus
from src.notification.domain.exceptions import CannotResendNotification


class CanResendNotificationService:
    def can_resend_notification(self, notification: Notification) -> None:
        if (
            notification.status is NotificationStatus.SENT
            or notification.status is NotificationStatus.SUCCESS
        ):
            raise CannotResendNotification(notification_id=str(notification.id_.value))
