import logging

import pytest  # noqa

from app.infrastructure.notifications.sms.logger_sms_notification_gateway import (
    LoggerSMSNotificationGateway,
)


async def test_logger_notification_gateway(caplog):
    module = "app.infrastructure.notifications.sms.logger_sms_notification_gateway"

    gateway = LoggerSMSNotificationGateway()

    with caplog.at_level(logging.INFO, logger=module):
        await gateway.send({"test": "test"})

    assert '{"test": "test"}' in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"
    assert caplog.records[0].message == '{"test": "test"}'
