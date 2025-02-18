from typing import Any

from app.domain.base.exceptions import DomainError, DomainValidationError


class InvalidLabourId(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Invalid Labour ID.")


class LabourHasActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot start a new contraction while one is active")


class CannotCompleteLabourWithActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot complete labor with active contraction")


class LabourHasNoActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("No active contraction to end")


class LabourAlreadyBegun(DomainError):
    def __init__(self) -> None:
        super().__init__("Labour has already begun")


class LabourAlreadyCompleted(DomainError):
    def __init__(self) -> None:
        super().__init__("Labour is already completed")


class LabourNotFoundById(DomainError):
    def __init__(self, labour_id: Any) -> None:
        super().__init__(f"Labour with id '{labour_id}' is not found.")
