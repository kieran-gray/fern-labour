import logging
from uuid import UUID

from src.application.dtos import ContactMessageDTO
from src.domain.contact_message_id import ContactMessageId
from src.domain.exceptions import ContactMessageNotFoundById, InvalidContactMessageId
from src.domain.repository import ContactMessageRepository

log = logging.getLogger(__name__)


class ContactMessageQueryService:
    def __init__(self, contact_message_repository: ContactMessageRepository):
        self._contact_message_repository = contact_message_repository

    async def get_message(self, contact_message_id: str) -> ContactMessageDTO:
        try:
            domain_id = ContactMessageId(UUID(contact_message_id))
        except ValueError:
            raise InvalidContactMessageId(contact_message_id=contact_message_id)

        contact_message = await self._contact_message_repository.get_by_id(
            contact_message_id=domain_id
        )
        if not contact_message:
            raise ContactMessageNotFoundById(contact_message_id=contact_message_id)

        return ContactMessageDTO.from_domain(contact_message=contact_message)
