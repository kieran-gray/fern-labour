from app.domain.base.exceptions import DomainValidationError
from app.domain.contraction.constants import CONTRACTION_MAX_INTENSITY, CONTRACTION_MIN_INTENSITY


class ContractionStartTimeAfterEndTime(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Start time cannot be after end time")


class ContractionIntensityInvalid(DomainValidationError):
    def __init__(self) -> None:
        max = CONTRACTION_MAX_INTENSITY
        min = CONTRACTION_MIN_INTENSITY
        super().__init__(f"Contraction intensity must be between {min} and {max}")
