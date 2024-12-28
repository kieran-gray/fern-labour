import logging

import pytest  # noqa

from app.infrastructure.notifications.email.logger_email_notification_gateway import (
    LoggerEmailNotificationGateway,
)


async def test_logger_notification_gateway(caplog):
    module = "app.infrastructure.notifications.email.logger_email_notification_gateway"

    gateway = LoggerEmailNotificationGateway()

    with caplog.at_level(logging.INFO, logger=module):
        await gateway.send({"test": "test"})

    assert '{"test": "test"}' in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"
    assert caplog.records[0].message == '{"test": "test"}'
