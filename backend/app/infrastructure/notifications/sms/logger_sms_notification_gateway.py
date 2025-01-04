import json
import logging
from typing import Any

from app.application.notifications.notfication_gateway import SMSNotificationGateway

log = logging.getLogger(__name__)


class LoggerSMSNotificationGateway(SMSNotificationGateway):
    """Notification gateway that logs sms notifications"""

    async def send(self, data: dict[str, Any]) -> None:
        log.info(json.dumps(data))
