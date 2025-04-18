import json
import logging

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.gateways.sms_notification_gateway import SMSNotificationGateway
from src.notification.domain.enums import NotificationStatus

log = logging.getLogger(__name__)


class LoggerSMSNotificationGateway(SMSNotificationGateway):
    """Notification gateway that logs sms notifications"""

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        log.info(json.dumps(notification.to_dict()))
        return NotificationSendResult(True, NotificationStatus.SENT)
