import logging
from typing import Any

from fern_labour_core.events.producer import EventProducer

from src.application.dtos import ContactMessageDTO
from src.domain.entity import ContactMessage
from src.domain.enums import ContactMessageCategory
from src.domain.exceptions import InvalidContactMessageCategory
from src.domain.repository import ContactMessageRepository
from src.user.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class ContactMessageService:
    def __init__(
        self,
        contact_message_repository: ContactMessageRepository,
        event_producer: EventProducer,
    ):
        self._contact_message_repository = contact_message_repository
        self._event_producer = event_producer

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
