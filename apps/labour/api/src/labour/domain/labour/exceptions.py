from typing import Any

from fern_labour_core.exceptions.domain import DomainError, DomainValidationError


class InvalidLabourId(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Invalid Labour ID.")


class InvalidLabourUpdateId(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Invalid Labour Update ID.")


class LabourHasActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot start a new contraction while one is active")


class CannotCompleteLabourWithActiveContraction(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot complete labour with active contraction")


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


class LabourUpdateNotFoundById(DomainError):
    def __init__(self, labour_update_id: Any) -> None:
        super().__init__(f"Labour Update with id '{labour_update_id}' is not found.")


class UnauthorizedLabourRequest(DomainError):
    def __init__(self) -> None:
        super().__init__("User is not authorized to access requested labour.")


class CannotDeleteActiveLabour(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot delete active labour.")


class CannotSubscribeToOwnLabour(DomainError):
    def __init__(self) -> None:
        super().__init__("Cannot subscribe to own labour")
