import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.application.alert_service import AlertService

log = logging.getLogger(__name__)


class SlackAlertService(AlertService):
    def __init__(self, token: str, channel: str, client: WebClient | None = None) -> None:
        self._client = client or WebClient(token=token)
        self._channel = channel

    async def send_alert(self, message: str) -> None:
        try:
            self._client.chat_postMessage(channel=self._channel, text=message)
        except SlackApiError as e:
            log.error(e.response["error"])
