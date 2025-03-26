import json
import logging

from app.application.dtos.notification import NotificationDTO, NotificationSendResult
from app.application.notifications.notfication_gateway import EmailNotificationGateway
from app.domain.notification.enums import NotificationStatus

log = logging.getLogger(__name__)


class LoggerEmailNotificationGateway(EmailNotificationGateway):
    """Notification gateway that logs emails"""

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        log.info(json.dumps(notification.to_dict()))
        return NotificationSendResult(True, NotificationStatus.SENT)
