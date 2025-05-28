from dataclasses import dataclass
from typing import Self
from unittest.mock import Mock

import pytest

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.domain.enums import NotificationStatus
from src.notification.infrastructure.gateways.twilio_sms_gateway import TwilioSMSNotificationGateway
from src.notification.infrastructure.twilio.status_mapping import TWILIO_STATUS_MAPPING


@dataclass
class MockMessage:
    sid: str
    status: str

    def fetch(self) -> Self:
        return self


@pytest.fixture
def gateway() -> TwilioSMSNotificationGateway:
    return TwilioSMSNotificationGateway(
        account_sid="test",
        auth_token="test",
        messaging_service_sid="test",
        client=Mock(),
    )


async def test_can_send_sms(gateway: TwilioSMSNotificationGateway) -> None:
    gateway._client.messages.create.return_value = MockMessage("ext123", "sent")
    notification = NotificationDTO(
        id="123",
        status="REQUESTED",
        channel="sms",
        destination="07123123123",
        template="labour_update",
        data={},
    )
    result = await gateway.send(notification)
    assert result == NotificationSendResult(
        success=True, status=NotificationStatus.SENT, external_id="ext123"
    )


async def test_can_get_status(gateway: TwilioSMSNotificationGateway) -> None:
    gateway._client.messages.return_value = MockMessage("ext123", "failed")
    result = await gateway.get_status("ext123")
    assert result == TWILIO_STATUS_MAPPING.get("failed")


async def test_other_status_returns_none(
    gateway: TwilioSMSNotificationGateway, caplog: pytest.LogCaptureFixture
) -> None:
    gateway._client.messages.return_value = MockMessage("ext123", "new_unknown_status")

    result = await gateway.get_status("ext123")
    assert result is None
    assert "Did not find notification status for notification" in caplog.text


async def test_redact_message_body(gateway: TwilioSMSNotificationGateway) -> None:
    gateway._client.messages.update.return_value = None

    result = await gateway.redact_notification_body("ext123")
    assert result is None
