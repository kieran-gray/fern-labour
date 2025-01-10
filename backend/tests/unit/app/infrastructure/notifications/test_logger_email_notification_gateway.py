import json
import logging

import pytest  # noqa

from app.application.notifications.entity import Notification
from app.infrastructure.notifications.email.logger_email_notification_gateway import (
    LoggerEmailNotificationGateway,
)


async def test_logger_notification_gateway(caplog):
    module = "app.infrastructure.notifications.email.logger_email_notification_gateway"

    gateway = LoggerEmailNotificationGateway()
    notification = Notification(
        type="email", message="message", destination="email@test.com", subject="test email"
    )

    with caplog.at_level(logging.INFO, logger=module):
        await gateway.send(notification)

    assert json.dumps(notification.to_dict()) in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"
