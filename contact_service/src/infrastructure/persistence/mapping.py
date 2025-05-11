from sqlalchemy.orm import composite

from src.domain.contact_message_id import ContactMessageId
from src.domain.entity import ContactMessage
from src.infrastructure.persistence.orm_registry import mapper_registry
from src.infrastructure.persistence.table import contact_messages_table


def map_contact_messages_table() -> None:
    mapper_registry.map_imperatively(
        ContactMessage,
        contact_messages_table,
        properties={
            "id_": composite(ContactMessageId, contact_messages_table.c.id),
            "category": contact_messages_table.c.category,
            "email": contact_messages_table.c.email,
            "name": contact_messages_table.c.name,
            "message": contact_messages_table.c.message,
            "data": contact_messages_table.c.data,
            "user_id": contact_messages_table.c.user_id,
        },
        column_prefix="_",
    )
