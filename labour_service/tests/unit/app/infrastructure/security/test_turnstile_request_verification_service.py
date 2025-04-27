from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.core.infrastructure.security.cloudflare.turnstile_request_verification_service import (
    TurnstileRequestVerificationService,
)
from src.core.infrastructure.security.interfaces.exceptions import (
    InvalidVerificationTokenException,
    RequestVerificationError,
    VerificationTokenAlreadyUsedException,
)


@pytest.fixture
def service() -> TurnstileRequestVerificationService:
    return TurnstileRequestVerificationService("/", "test")


async def test_can_verify_token(service: TurnstileRequestVerificationService):
    mock = AsyncMock()
    mock.return_value = {"success": True, "error-codes": []}
    service._call_cloudflare_api = mock

    result = await service.verify("token", "1.1.1.1")
    assert result is None


async def test_unsuccessful_verification_raises_error(service: TurnstileRequestVerificationService):
    mock = AsyncMock()
    mock.return_value = {"success": False, "error-codes": []}
    service._call_cloudflare_api = mock

    with pytest.raises(RequestVerificationError):
        await service.verify("token", "1.1.1.1")


async def test_timeout_or_duplicate_raises_error(service: TurnstileRequestVerificationService):
    mock = AsyncMock()
    mock.return_value = {"success": False, "error-codes": ["timeout-or-duplicate"]}
    service._call_cloudflare_api = mock

    with pytest.raises(VerificationTokenAlreadyUsedException):
        await service.verify("token", "1.1.1.1")


async def test_invalid_input_raises_error(service: TurnstileRequestVerificationService):
    mock = AsyncMock()
    mock.return_value = {"success": False, "error-codes": ["invalid-input-response"]}
    service._call_cloudflare_api = mock

    with pytest.raises(InvalidVerificationTokenException):
        await service.verify("token", "1.1.1.1")


@patch("httpx.AsyncClient")
async def test_call_cloudflare_api_success(
    mock_client, service: TurnstileRequestVerificationService
):
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance

    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "error-codes": []}
    mock_client_instance.post.return_value = mock_response

    result = await service.verify("test_token", "127.0.0.1")

    assert result is None
