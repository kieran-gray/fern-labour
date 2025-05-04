import json
import logging
from uuid import uuid4

import pytest  # noqa

from src.notification.application.dtos.notification import NotificationDTO
from src.notification.domain.enums import NotificationStatus
from src.notification.infrastructure.gateways.log_gateway import (
    LogNotificationGateway,
)


async def test_log_notification_gateway(caplog):
    module = "src.notification.infrastructure.gateways.log_gateway"

    gateway = LogNotificationGateway()

    notification = NotificationDTO(
        id=str(uuid4()),
        status=NotificationStatus.CREATED.value,
        channel="sms",
        template="template.html",
        data={"test": "test"},
        destination="+44123123123",
    )

    with caplog.at_level(logging.INFO, logger=module):
        await gateway.send(notification)

    assert json.dumps(notification.to_dict()) in caplog.text
    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == "INFO"
