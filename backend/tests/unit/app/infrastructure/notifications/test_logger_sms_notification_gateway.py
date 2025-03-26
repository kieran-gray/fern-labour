import json
import logging
from uuid import uuid4

import pytest  # noqa

from app.application.dtos.notification import NotificationDTO
from app.domain.notification.enums import NotificationStatus
from app.infrastructure.notifications.sms.logger_sms_notification_gateway import (
    LoggerSMSNotificationGateway,
)


async def test_logger_notification_gateway(caplog):
    module = "app.infrastructure.notifications.sms.logger_sms_notification_gateway"

    gateway = LoggerSMSNotificationGateway()

    notification = NotificationDTO(
        id=str(uuid4()),
        status=NotificationStatus.CREATED.value,
        type="sms",
        template="template.html",
        data={"test": "test"},
        destination="+44123123123",
    )

    with caplog.at_level(logging.INFO, logger=module):
        await gateway.send(notification)

    assert json.dumps(notification.to_dict()) in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"
