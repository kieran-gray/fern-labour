from uuid import UUID

from app.domain.base.exceptions import DomainError


class UserAlreadyHasActiveLaborSession(DomainError):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already has an active labor session")


class LaborSessionHasActiveContraction(DomainError):
    def __init__(self):
        super().__init__("Cannot start a new contraction while one is active")


class CannotCompleteLaborSessionWithActiveContraction(DomainError):
    def __init__(self):
        super().__init__("Cannot complete labor with active contraction")


class LaborSessionHasNoActiveContraction(DomainError):
    def __init__(self):
        super().__init__("No active contraction to end")


class LaborSessionCompleted(DomainError):
    def __init__(self):
        super().__init__("Cannot add contractions to a completed labor session")


class LaborSessionNotFoundById(DomainError):
    def __init__(self, labor_session_id: UUID):
        super().__init__(f"Labor session not found with ID: {labor_session_id}")
