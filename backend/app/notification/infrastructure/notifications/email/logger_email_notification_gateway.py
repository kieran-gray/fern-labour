import json
import logging

from app.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from app.notification.application.gateways.email_notification_gateway import (
    EmailNotificationGateway,
)
from app.notification.domain.enums import NotificationStatus

log = logging.getLogger(__name__)


class LoggerEmailNotificationGateway(EmailNotificationGateway):
    """Notification gateway that logs emails"""

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        log.info(json.dumps(notification.to_dict()))
        return NotificationSendResult(True, NotificationStatus.SENT)
