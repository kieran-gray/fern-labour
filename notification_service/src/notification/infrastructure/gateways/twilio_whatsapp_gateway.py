import logging

from twilio.rest import Client

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.interfaces.notification_gateway import WhatsAppNotificationGateway
from src.notification.domain.enums import NotificationStatus
from src.notification.infrastructure.twilio.status_mapping import TWILIO_STATUS_MAPPING

log = logging.getLogger(__name__)


class TwilioWhatsAppNotificationGateway(WhatsAppNotificationGateway):
    """
    Notification gateway that sends WhatsApp messages

    Business initiated WhatsApp messages are required to use templates.
    These templates are defined in twilio and need approval from Meta.
    """

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        messaging_service_sid: str | None = None,
        client: Client | None = None,
    ):
        self._client = client or Client(username=account_sid, password=auth_token)
        self._messaging_service_sid = messaging_service_sid

    async def send(self, notification: NotificationDTO) -> NotificationSendResult:
        message = self._client.messages.create(
            content_sid=notification.subject,
            content_variables=notification.message,
            messaging_service_sid=self._messaging_service_sid,
            to=notification.destination,
        )
        log.info(f"Sent SMS notification id {notification.id}")

        return NotificationSendResult(
            success=True, status=NotificationStatus.SENT, external_id=message.sid
        )

    async def get_status(self, external_id: str) -> str:
        log.debug(f"Fetching status for notification {external_id=}")

        message = self._client.messages(sid=external_id).fetch()
        if status := TWILIO_STATUS_MAPPING.get(message.status):
            return status

        log.warning(f"Did not find notification status for notification {external_id=}")
        return NotificationStatus.SENT
