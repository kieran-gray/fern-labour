import json
import logging

from app.application.dtos.notification import NotificationDTO, NotificationSendResult
from app.application.notifications.notfication_gateway import SMSNotificationGateway
from app.domain.notification.enums import NotificationStatus

log = logging.getLogger(__name__)


class LoggerSMSNotificationGateway(SMSNotificationGateway):
    """Notification gateway that logs sms notifications"""

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        log.info(json.dumps(notification.to_dict()))
        return NotificationSendResult(True, NotificationStatus.SENT)
