from datetime import datetime
from uuid import UUID

from app.application.dtos.contraction_dto import ContractionDTO
from app.application.dtos.labor_session_dto import LaborSessionDTO
from app.application.services.user_service import UserService
from app.domain.entities.labor_session import LaborSession
from app.domain.exceptions.labor_session import (
    LaborSessionNotFoundById,
    UserAlreadyHasActiveLaborSession,
)
from app.domain.exceptions.user import UserNotFoundById
from app.domain.repositories.labor_session_repository import LaborSessionRepository

# from app.domain.services.notification_service import NotificationService


class LaborSessionService:
    """
    Application service for managing labor session functionality.
    Coordinates between domain entities and infrastructure services.
    """

    def __init__(
        self,
        labor_session_repository: LaborSessionRepository,
        user_service: UserService,
    ):
        self._labor_session_repo = labor_session_repository
        self._user_service = user_service

    async def start_labor_session(self, user_id: UUID, first_labor: bool) -> LaborSessionDTO:
        """
        Start a new labor session for a user.

        Args:
            user_id: ID of the user starting labor

        Returns:
            DTO representing the new labor session
        """
        user = await self._user_service.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundById()

        active_session = await self._labor_session_repo.get_active_session(user_id)
        if active_session:
            raise UserAlreadyHasActiveLaborSession(user.username)

        labor_session = LaborSession.start(user_id=user_id, first_labor=first_labor)
        await self._labor_session_repo.save(labor_session)

        return LaborSessionDTO.from_domain(labor_session)

    async def start_contraction(
        self, session_id: UUID, intensity: int, notes: str | None = None
    ) -> ContractionDTO:
        """
        Start a new contraction in a labor session.

        Args:
            session_id: ID of the labor session
            intensity: Intensity of the contraction (1-10)
            notes: Optional notes about the contraction

        Returns:
            DTO representing the new contraction
        """
        session = await self._labor_session_repo.get_by_id(session_id)
        if not session:
            raise LaborSessionNotFoundById(session_id)

        contraction = session.start_contraction(intensity=intensity, notes=notes)
        await self._labor_session_repo.save(session)

        return ContractionDTO.from_domain(contraction)

    async def end_contraction(self, session_id: UUID) -> ContractionDTO:
        """
        End the active contraction in a labor session.

        Args:
            session_id: ID of the labor session

        Returns:
            DTO representing the ended contraction
        """
        session = await self._labor_session_repo.get_by_id(session_id)
        if not session:
            raise LaborSessionNotFoundById(session_id)

        session.end_contraction(datetime.now())
        await self._labor_session_repo.save(session)

        # Notify that it is time to go to hospital

        return ContractionDTO.from_domain(session.contractions[-1])

    async def get_session_summary(self, session_id: UUID) -> dict:
        """
        Get a summary of the current labor session.

        Args:
            session_id: ID of the labor session

        Returns:
            Dictionary containing session summary
        """
        session = await self._labor_session_repo.get_by_id(session_id)
        if not session:
            raise LaborSessionNotFoundById(session_id)

        return {
            "session_id": session.id_.value,
            "duration": (datetime.now() - session.start_time).total_seconds() / 3600,
            "contraction_count": len(session.contractions),
            "current_phase": session.current_phase.value,
            "hospital_recommended": session.should_go_to_hospital,
            "pattern": session.get_contraction_pattern(),
        }

    async def complete_session(self, session_id: UUID, notes: str | None = None) -> LaborSessionDTO:
        """
        Mark a labor session as complete.

        Args:
            session_id: ID of the labor session
            notes: Optional notes about the completion

        Returns:
            DTO representing the completed session
        """
        session = await self._labor_session_repo.get_by_id(session_id)
        if not session:
            raise LaborSessionNotFoundById(session_id)

        session.complete_labor(notes=notes)
        await self._labor_session_repo.save(session)

        return LaborSessionDTO.from_domain(session)

    async def get_user_sessions(
        self, user_id: UUID, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> list[LaborSessionDTO]:
        """
        Get all labor sessions for a user, optionally filtered by date range.

        Args:
            user_id: ID of the user
            start_date: Optional start of date range
            end_date: Optional end of date range

        Returns:
            List of labor session DTOs
        """
        if start_date and end_date:
            sessions = await self._labor_session_repo.get_sessions_between(
                user_id, start_date, end_date
            )
        else:
            sessions = await self._labor_session_repo.get_by_user_id(user_id)

        return [LaborSessionDTO.from_domain(session) for session in sessions]
