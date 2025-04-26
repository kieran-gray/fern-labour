from typing import Any

import pytest

from src.notification.application.exceptions import UnauthorizedWebhookRequest
from src.notification.infrastructure.twilio.twilio_request_verification_service import (
    TwilioRequestVerificationService,
)


class MockSuccessValidator:
    def validate(self, uri: Any, params: Any, signature: Any) -> bool:
        return True


class MockFailureValidator:
    def validate(self, uri: Any, params: Any, signature: Any) -> bool:
        return False


def test_valid_request_returns_none():
    service = TwilioRequestVerificationService("test", MockSuccessValidator())
    assert service.verify("test", "test", "test") is None


def test_invalid_request_raises_exception():
    service = TwilioRequestVerificationService("test", MockFailureValidator())
    with pytest.raises(UnauthorizedWebhookRequest):
        service.verify("test", "test", "test")
