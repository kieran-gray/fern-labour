import json
import logging
from typing import Any

from twilio.rest import Client

from app.application.notifications.notfication_gateway import SMSNotificationGateway
from app.setup.settings import Settings

log = logging.getLogger(__name__)


class TwilioSMSNotificationGateway(SMSNotificationGateway):
    """Notification gateway that sends SMS"""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = Client(
            username=self._settings.notifications.twilio.account_sid,
            password=self._settings.notifications.twilio.auth_token,
        )

    def send(self, data: dict[str, Any]) -> None:
        twilio_settings = self._settings.notifications.twilio
        assert twilio_settings.twilio_enabled

        destination_phone_number = "+447808006430"  # TODO enrich event

        message = self._client.messages.create(
            body=json.dumps(data),
            from_=twilio_settings.sms_from_number,
            to=destination_phone_number,
        )

        log.info(f"Sent SMS notification of event {data["type"]} to contact")
        log.debug(message.body)
