from app.domain.base.exceptions import DomainError, DomainValidationError
from app.domain.constants.contraction import CONTRACTION_MAX_INTENSITY, CONTRACTION_MIN_INTENSITY


class ContractionOverlaps(DomainError):
    def __init__(self):
        super().__init__("Contractions cannot overlap")


class ContractionStartTimeAfterEndTime(DomainValidationError):
    def __init__(self):
        super().__init__("Start time cannot be after end time")


class ContractionDurationExceedsMaxDuration(DomainValidationError):
    def __init__(self):
        super().__init__("Contraction duration cannot exceed maximum length")


class ContractionDurationLessThanMinDuration(DomainValidationError):
    def __init__(self):
        super().__init__("Contraction duration under minimum length")


class ContractionIntensityInvalid(DomainValidationError):
    def __init__(self):
        max = CONTRACTION_MAX_INTENSITY
        min = CONTRACTION_MIN_INTENSITY
        super().__init__(f"Contraction intensity must be between {min} and {max}")
