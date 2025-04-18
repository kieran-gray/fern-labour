import json
import logging

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.interfaces.notification_gateway import NotificationGateway
from src.notification.domain.enums import NotificationStatus

log = logging.getLogger(__name__)


class LogNotificationGateway(NotificationGateway):
    """Notification gateway that logs notification."""

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        log.info(json.dumps(notification.to_dict()))
        return NotificationSendResult(True, NotificationStatus.SENT)
