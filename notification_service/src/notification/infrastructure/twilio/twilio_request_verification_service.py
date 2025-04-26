import logging
from typing import Any

from twilio.request_validator import RequestValidator

from src.notification.application.exceptions import UnauthorizedWebhookRequest
from src.notification.infrastructure.security.request_verification_service import (
    RequestVerificationService,
)

log = logging.getLogger(__name__)


class TwilioRequestVerificationService(RequestVerificationService):
    def __init__(self, auth_token: str, request_validator: RequestValidator | None = None):
        self._request_validator = request_validator or RequestValidator(token=auth_token)

    def verify(self, uri: Any, params: Any, signature: Any) -> None:
        log.debug(f"Twilio Request Verification for ({uri=}, {params=}, {signature=})")
        verified = self._request_validator.validate(uri=uri, params=params, signature=signature)
        if not verified:
            raise UnauthorizedWebhookRequest()
