from typing import Any

from fern_labour_core.exceptions.domain import DomainError, DomainValidationError


class InvalidContactMessageCategory(DomainValidationError):
    def __init__(self, category: Any) -> None:
        super().__init__(f"Invalid Contact Message Category '{category}'")


class InvalidContactMessageId(DomainValidationError):
    def __init__(self, contact_message_id: Any) -> None:
        super().__init__(f"Invalid Contact Message Id '{contact_message_id}'")


class ContactMessageNotFoundById(DomainError):
    def __init__(self, contact_message_id: Any) -> None:
        super().__init__(f"Contact Message with Id '{contact_message_id}' not found")
