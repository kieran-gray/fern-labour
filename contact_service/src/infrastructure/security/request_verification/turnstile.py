import logging
from typing import Any
from uuid import uuid4

import httpx

from src.infrastructure.security.request_verification.exceptions import (
    InvalidVerificationTokenException,
    RequestVerificationError,
    VerificationTokenAlreadyUsedException,
)
from src.infrastructure.security.request_verification.interface import (
    RequestVerificationService,
)

log = logging.getLogger(__name__)


class TurnstileRequestVerificationService(RequestVerificationService):
    """Request verification by token with Cloudflare Turnstile"""

    def __init__(self, cloudflare_url: str, cloudflare_secret_key: str):
        self._cloudflare_url = cloudflare_url
        self._cloudflare_secret_key = cloudflare_secret_key
        self._error_codes = [
            "invalid-input-response",
            "timeout-or-duplicate",
        ]

    async def _call_cloudflare_api(self, token: str, ip: str) -> Any:
        idempotency_key = uuid4()  # TODO is this really doing anything?
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=self._cloudflare_url,
                json={
                    "secret": self._cloudflare_secret_key,
                    "response": token,
                    "remoteip": ip,
                    "idempotency_key": str(idempotency_key),
                },
                headers={"Content-Type": "application/json"},
            )
            return response.json()

    async def verify(self, token: str, ip: str) -> None:
        """
        Verify the given token and return bool indicating success or failure.
        """
        result = await self._call_cloudflare_api(token, ip)
        if not result["success"]:
            log.error(f"Request verification failed: {result}")
            if "timeout-or-duplicate" in result["error-codes"]:
                raise VerificationTokenAlreadyUsedException()
            if "invalid-input-response" in result["error-codes"]:
                raise InvalidVerificationTokenException()
            raise RequestVerificationError("Request verification with turnstile failed.")
