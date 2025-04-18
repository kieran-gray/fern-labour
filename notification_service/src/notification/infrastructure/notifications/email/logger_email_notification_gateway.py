import json
import logging

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.gateways.email_notification_gateway import (
    EmailNotificationGateway,
)
from src.notification.domain.enums import NotificationStatus

log = logging.getLogger(__name__)


class LoggerEmailNotificationGateway(EmailNotificationGateway):
    """Notification gateway that logs emails"""

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        log.info(json.dumps(notification.to_dict()))
        return NotificationSendResult(True, NotificationStatus.SENT)
