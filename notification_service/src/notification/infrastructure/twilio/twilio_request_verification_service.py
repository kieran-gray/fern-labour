from typing import Any

from twilio.request_validator import RequestValidator

from src.notification.application.exceptions import UnauthorizedWebhookRequest
from src.notification.infrastructure.security.request_verification_service import (
    RequestVerificationService,
)


class TwilioRequestVerificationService(RequestVerificationService):
    def __init__(self, auth_token: str):
        self._request_validator = RequestValidator(token=auth_token)

    def verify(self, uri: Any, params: Any, signature: Any) -> None:
        verified = self._request_validator.validate(uri=uri, params=params, signature=signature)
        if not verified:
            raise UnauthorizedWebhookRequest()
