import json
import logging
from uuid import uuid4

import pytest  # noqa

from app.notification.application.dtos.notification import NotificationDTO
from app.notification.domain.enums import NotificationStatus
from app.notification.infrastructure.notifications.email.logger_email_notification_gateway import (
    LoggerEmailNotificationGateway,
)


async def test_logger_notification_gateway(caplog):
    module = "app.notification.infrastructure.notifications.email.logger_email_notification_gateway"

    gateway = LoggerEmailNotificationGateway()
    notification = NotificationDTO(
        id=str(uuid4()),
        status=NotificationStatus.CREATED.value,
        type="email",
        template="template.html",
        data={"test": "test"},
        destination="email@test.com",
    )

    with caplog.at_level(logging.INFO, logger=module):
        await gateway.send(notification)

    assert json.dumps(notification.to_dict()) in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"
