import logging
from dataclasses import dataclass
from typing import Any

from fern_labour_core.events.producer import EventProducer
from fern_labour_notifications_shared.enums import NotificationChannel, NotificationTemplate
from fern_labour_notifications_shared.events import NotificationRequested
from fern_labour_notifications_shared.notification_data import ContactUsData

from src.application.dtos import ContactMessageDTO
from src.domain.entity import ContactMessage
from src.domain.enums import ContactMessageCategory
from src.domain.exceptions import InvalidContactMessageCategory
from src.domain.repository import ContactMessageRepository
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


@dataclass
class ContactNotificationMetadata:
    from_user_id: str

    def to_dict(self) -> dict[str, str]:
        return {"from_user_id": self.from_user_id}


class ContactMessageService:
    def __init__(
        self,
        contact_message_repository: ContactMessageRepository,
        event_producer: EventProducer,
        contact_email: str,
    ):
        self._contact_message_repository = contact_message_repository
        self._event_producer = event_producer
        self._contact_email = contact_email
        self._template = NotificationTemplate.CONTACT_US_SUBMISSION

    async def create_message(
        self,
        category: str,
        email: str,
        name: str,
        message: str,
        data: dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> ContactMessageDTO:
        try:
            domain_category = ContactMessageCategory(category)
        except ValueError:
            raise InvalidContactMessageCategory(category=category)

        contact_message = ContactMessage.create(
            category=domain_category,
            email=email,
            name=name,
            message=message,
            data=data,
            user_id=UserId(user_id) if user_id else None,
        )

        await self._contact_message_repository.save(contact_message=contact_message)

        await self._event_producer.publish_batch(contact_message.clear_domain_events())

        return ContactMessageDTO.from_domain(contact_message=contact_message)

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
