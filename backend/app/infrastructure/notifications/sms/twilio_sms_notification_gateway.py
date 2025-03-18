import logging

from twilio.rest import Client

from app.application.notifications.entity import Notification
from app.application.notifications.notfication_gateway import SMSNotificationGateway

log = logging.getLogger(__name__)


class TwilioSMSNotificationGateway(SMSNotificationGateway):
    """Notification gateway that sends SMS"""

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        sms_from_number: str | None = None,
        messaging_service_sid: str | None = None,
    ):
        self._client = Client(username=account_sid, password=auth_token)
        self._sms_from_number = sms_from_number
        self._messaging_service_sid = messaging_service_sid

    async def send(self, notification: Notification) -> None:
        # TODO I could update message delivery status
        self._client.messages.create(
            body=notification.message,
            messaging_service_sid=self._messaging_service_sid,
            to=notification.destination,
        )
        log.info("Sent sms notification")
