import json
import logging

import pytest  # noqa

from app.application.notifications.entity import Notification
from app.infrastructure.notifications.sms.logger_sms_notification_gateway import (
    LoggerSMSNotificationGateway,
)


async def test_logger_notification_gateway(caplog):
    module = "app.infrastructure.notifications.sms.logger_sms_notification_gateway"

    gateway = LoggerSMSNotificationGateway()

    notification = Notification(
        type="sms", message="message", destination="email@test.com", subject="test email"
    )

    with caplog.at_level(logging.INFO, logger=module):
        await gateway.send(notification)

    assert json.dumps(notification.to_dict()) in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"
