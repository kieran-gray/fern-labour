from typing import Any

from app.domain.base.exceptions import DomainError


class LabourHasActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot start a new contraction while one is active")


class CannotCompleteLabourWithActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot complete labor with active contraction")


class LabourHasNoActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("No active contraction to end")


class LabourCompleted(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot start contraction for completed labour")


class LabourNotFoundById(DomainError):
    def __init__(self, labour_id: Any) -> None:
        super().__init__(f"Labour with id '{labour_id}' is not found.")
