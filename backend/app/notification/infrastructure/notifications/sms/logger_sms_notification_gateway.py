import json
import logging

from app.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from app.notification.application.gateways.sms_notification_gateway import SMSNotificationGateway
from app.notification.domain.enums import NotificationStatus

log = logging.getLogger(__name__)


class LoggerSMSNotificationGateway(SMSNotificationGateway):
    """Notification gateway that logs sms notifications"""

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        log.info(json.dumps(notification.to_dict()))
        return NotificationSendResult(True, NotificationStatus.SENT)
