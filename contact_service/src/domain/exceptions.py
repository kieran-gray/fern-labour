from typing import Any

from fern_labour_core.exceptions.domain import DomainError


class InvalidContactMessageCategory(DomainError):
    def __init__(self, category: Any) -> None:
        super().__init__(f"Invalid Contact Message Category '{category}'")
