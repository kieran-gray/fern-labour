from unittest.mock import Mock, patch

import pytest
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.infrastructure.slack.slack_alert_service import SlackAlertService


@pytest.fixture
def mock_client():
    return Mock(spec=WebClient)


@pytest.fixture
def slack_alert_service(mock_client) -> SlackAlertService:
    return SlackAlertService(token="xoxb-test-token", channel="#test-channel", client=mock_client)


def test_init_with_provided_client(mock_client):
    service = SlackAlertService(
        token="xoxb-test-token", channel="#test-channel", client=mock_client
    )

    assert service._client is mock_client
    assert service._channel == "#test-channel"


def test_init_without_provided_client():
    with patch("src.infrastructure.slack.slack_alert_service.WebClient") as mock_webclient_class:
        mock_client_instance = Mock()
        mock_webclient_class.return_value = mock_client_instance

        service = SlackAlertService(token="xoxb-test-token", channel="#test-channel")

        mock_webclient_class.assert_called_once_with(token="xoxb-test-token")
        assert service._client is mock_client_instance
        assert service._channel == "#test-channel"


async def test_send_alert_success(slack_alert_service: SlackAlertService):
    message = "Test alert message"
    slack_alert_service._client.chat_postMessage.return_value = {"ok": True}

    await slack_alert_service.send_alert(message)

    slack_alert_service._client.chat_postMessage.assert_called_once_with(
        channel="#test-channel", text=message
    )


async def test_send_alert_slack_api_error(
    slack_alert_service: SlackAlertService, caplog: pytest.LogCaptureFixture
):
    message = "Test alert message"
    error_response = {"error": "channel_not_found"}
    slack_error = SlackApiError("Channel not found", error_response)
    slack_alert_service._client.chat_postMessage.side_effect = slack_error

    await slack_alert_service.send_alert(message)

    slack_alert_service._client.chat_postMessage.assert_called_once_with(
        channel="#test-channel", text=message
    )
    assert "channel_not_found" in caplog.text


async def test_send_alert_with_empty_message(slack_alert_service: SlackAlertService):
    message = ""
    slack_alert_service._client.chat_postMessage.return_value = {"ok": True}

    await slack_alert_service.send_alert(message)

    slack_alert_service._client.chat_postMessage.assert_called_once_with(
        channel="#test-channel", text=message
    )


async def test_send_alert_with_multiline_message(slack_alert_service: SlackAlertService):
    message = "Multi\nline\nmessage"

    await slack_alert_service.send_alert(message)

    slack_alert_service._client.chat_postMessage.assert_called_once_with(
        channel="#test-channel", text=message
    )


async def test_send_alert_with_unicode_message(slack_alert_service: SlackAlertService):
    message = "Message with unicode: 🚨 Alert! 🚨"

    await slack_alert_service.send_alert(message)

    slack_alert_service._client.chat_postMessage.assert_called_once_with(
        channel="#test-channel", text=message
    )


async def test_send_alert_with_special_characters(slack_alert_service: SlackAlertService):
    message = "Message with special chars: !@#$%^&*()"

    await slack_alert_service.send_alert(message)

    slack_alert_service._client.chat_postMessage.assert_called_once_with(
        channel="#test-channel", text=message
    )


async def test_send_alert_channel_not_found_error(
    slack_alert_service: SlackAlertService, caplog: pytest.LogCaptureFixture
):
    error_response = {"error": "channel_not_found"}
    slack_error = SlackApiError("Channel not found", error_response)
    slack_alert_service._client.chat_postMessage.side_effect = slack_error

    await slack_alert_service.send_alert("test message")

    assert "channel_not_found" in caplog.text


async def test_send_alert_not_in_channel_error(
    slack_alert_service: SlackAlertService, caplog: pytest.LogCaptureFixture
):
    error_response = {"error": "not_in_channel"}
    slack_error = SlackApiError("Not in channel", error_response)
    slack_alert_service._client.chat_postMessage.side_effect = slack_error

    await slack_alert_service.send_alert("test message")

    assert "not_in_channel" in caplog.text


async def test_send_alert_invalid_auth_error(
    slack_alert_service: SlackAlertService, caplog: pytest.LogCaptureFixture
):
    error_response = {"error": "invalid_auth"}
    slack_error = SlackApiError("Invalid auth", error_response)
    slack_alert_service._client.chat_postMessage.side_effect = slack_error

    await slack_alert_service.send_alert("test message")

    assert "invalid_auth" in caplog.text


async def test_send_alert_rate_limited_error(
    slack_alert_service: SlackAlertService, caplog: pytest.LogCaptureFixture
):
    error_response = {"error": "rate_limited"}
    slack_error = SlackApiError("Rate limited", error_response)
    slack_alert_service._client.chat_postMessage.side_effect = slack_error

    await slack_alert_service.send_alert("test message")

    assert "rate_limited" in caplog.text


async def test_send_alert_with_none_message(slack_alert_service: SlackAlertService):
    await slack_alert_service.send_alert(None)

    slack_alert_service._client.chat_postMessage.assert_called_once_with(
        channel="#test-channel", text=None
    )


def test_inheritance_from_alert_service():
    from src.application.alert_service import AlertService

    with patch("src.infrastructure.slack.slack_alert_service.WebClient"):
        service = SlackAlertService(token="test", channel="#test")
        assert isinstance(service, AlertService)


async def test_send_alert_preserves_client_state(slack_alert_service: SlackAlertService):
    original_client = slack_alert_service._client
    original_channel = slack_alert_service._channel

    await slack_alert_service.send_alert("test message")

    assert slack_alert_service._client is original_client
    assert slack_alert_service._channel == original_channel
