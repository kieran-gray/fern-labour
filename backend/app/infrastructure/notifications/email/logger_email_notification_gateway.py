import json
import logging

from app.application.notifications.entity import Notification
from app.application.notifications.notfication_gateway import EmailNotificationGateway

log = logging.getLogger(__name__)


class LoggerEmailNotificationGateway(EmailNotificationGateway):
    """Notification gateway that logs emails"""

    async def send(self, notification: Notification) -> None:
        log.info(json.dumps(notification.to_dict()))
