import json
import logging
from typing import Any

from app.application.notifications.notfication_gateway import EmailNotificationGateway

log = logging.getLogger(__name__)


class LoggerEmailNotificationGateway(EmailNotificationGateway):
    """Notification gateway that logs emails"""

    async def send(self, data: dict[str, Any]) -> None:
        log.info(json.dumps(data))
