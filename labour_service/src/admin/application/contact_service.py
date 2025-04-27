import logging
from dataclasses import dataclass

from src.core.domain.producer import EventProducer
from src.notification.enums import NotificationChannel, NotificationTemplate
from src.notification.events import NotificationRequested
from src.notification.notification_data import ContactUsData

log = logging.getLogger(__name__)


@dataclass
class ContactNotificationMetadata:
    from_user_id: str

    def to_dict(self) -> dict[str, str]:
        return {"from_user_id": self.from_user_id}


class ContactService:
    def __init__(
        self,
        event_producer: EventProducer,
        contact_email: str,
    ):
        self._event_producer = event_producer
        self._contact_email = contact_email
        self._template = NotificationTemplate.CONTACT_US_SUBMISSION

    def _generate_notification_data(
        self, email: str, name: str, message: str, user_id: str | None = None
    ) -> ContactUsData:
        return ContactUsData(email=email, name=name, message=message, user_id=user_id or "")

    async def send_contact_email(
        self, email: str, name: str, message: str, user_id: str | None = None
    ) -> None:
        log.info(f"Contact us submission for email = {email} Userid = {user_id}")
        notification_data = self._generate_notification_data(
            email=email, name=name, message=message, user_id=user_id
        )
        notification_metadata = ContactNotificationMetadata(from_user_id=user_id or "null")
        notification_event = NotificationRequested.create(
            data={
                "channel": NotificationChannel.EMAIL,
                "destination": self._contact_email,
                "template": self._template.value,
                "data": notification_data.to_dict(),
                "metadata": notification_metadata.to_dict(),
            }
        )
        await self._event_producer.publish(event=notification_event)
