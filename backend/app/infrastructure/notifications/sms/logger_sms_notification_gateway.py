import json
import logging

from app.application.notifications.entity import Notification
from app.application.notifications.notfication_gateway import SMSNotificationGateway

log = logging.getLogger(__name__)


class LoggerSMSNotificationGateway(SMSNotificationGateway):
    """Notification gateway that logs sms notifications"""

    async def send(self, notification: Notification) -> None:
        log.info(json.dumps(notification.to_dict()))
