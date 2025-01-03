import logging
from typing import Any

from twilio.rest import Client

from app.application.notifications.notfication_gateway import SMSNotificationGateway

log = logging.getLogger(__name__)


class TwilioSMSNotificationGateway(SMSNotificationGateway):
    """Notification gateway that sends SMS"""

    def __init__(self, account_sid: str, auth_token: str, sms_from_number: str):
        self._client = Client(username=account_sid, password=auth_token)
        self._sms_from_number = sms_from_number

    async def send(self, data: dict[str, Any]) -> None:
        message = self._client.messages.create(
            body=data["message"],
            from_=self._sms_from_number,
            to=data["destination"],
        )
        log.info("Sent email notification")
        log.debug(message.body)
