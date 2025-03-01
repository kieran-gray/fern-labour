from typing import Any

from app.domain.base.exceptions import DomainError, DomainValidationError
from app.domain.contraction.constants import CONTRACTION_MAX_INTENSITY, CONTRACTION_MIN_INTENSITY


class ContractionStartTimeAfterEndTime(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Start time cannot be after end time")


class ContractionIntensityInvalid(DomainValidationError):
    def __init__(self) -> None:
        max = CONTRACTION_MAX_INTENSITY
        min = CONTRACTION_MIN_INTENSITY
        super().__init__(f"Contraction intensity must be between {min} and {max}")


class ContractionIdInvalid(DomainValidationError):
    def __init__(self, contraction_id: Any) -> None:
        super().__init__(f"Contraction id '{contraction_id}' is invalid.")


class ContractionsOverlappingAfterUpdate(DomainError):
    def __init__(self) -> None:
        super().__init__("Invalid update causes contractions to overlap.")


class ContractionNotFoundById(DomainError):
    def __init__(self, contraction_id: Any) -> None:
        super().__init__(f"Contraction with id '{contraction_id}' is not found.")


class CannotUpdateActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot edit active contraction. Complete the contraction first.")
