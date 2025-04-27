from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.domain.enums import NotificationStatus
from src.notification.infrastructure.gateways.twilio_sms_gateway import TwilioSMSNotificationGateway


@dataclass
class MockMessage:
    sid: str


@pytest.fixture
def gateway() -> TwilioSMSNotificationGateway:
    return TwilioSMSNotificationGateway(
        account_sid="test",
        auth_token="test",
        messaging_service_sid="test",
        client=Mock(),
    )


async def test_can_send_sms(gateway: TwilioSMSNotificationGateway) -> None:
    gateway._client.messages.create.return_value = MockMessage("ext123")
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
