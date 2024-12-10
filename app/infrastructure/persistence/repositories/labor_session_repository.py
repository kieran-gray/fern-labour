from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.labor_session import LaborSession
from app.domain.repositories.labor_session_repository import LaborSessionRepository
from app.infrastructure.persistence.tables import labor_sessions


class SQLAlchemyLaborSessionRepository(LaborSessionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, labor_session: LaborSession) -> None:
        """
        Save or update a labor session.

        Args:
            labor_session: The labor session to save
        """
        self._session.add(labor_session)
        await self._session.commit()

    async def delete(self, labor_session: LaborSession) -> None:
        """
        Delete a labor session.

        Args:
            labor_session: The labor session to delete
        """
        self._session.delete(labor_session)
        await self._session.commit()

    async def get_by_id(self, session_id: UUID) -> LaborSession | None:
        """
        Retrieve a labor session by its ID.

        Args:
            session_id: The ID of the labor session to retrieve

        Returns:
            The labor session if found, None otherwise
        """
        stmt = (
            select(LaborSession)
            .options(selectinload(LaborSession.contractions))
            .where(labor_sessions.c.id == session_id)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> list[LaborSession]:
        """
        Retrieve all labor sessions for a given user.

        Args:
            user_id: The ID of the user

        Returns:
            List of labor sessions
        """
        stmt = (
            select(LaborSession)
            .options(selectinload(LaborSession.contractions))
            .where(labor_sessions.c.user_id == user_id)
        )

        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_session(self, user_id: UUID) -> LaborSession | None:
        """
        Retrieve the active labor session for a user, if any exists.
        A user should only have one active session at a time.

        Args:
            user_id: The ID of the user

        Returns:
            The active labor session if found, None otherwise
        """
        stmt = (
            select(LaborSession)
            .options(selectinload(LaborSession.contractions))
            .where(labor_sessions.c.user_id == user_id, labor_sessions.c.end_time.is_(None))
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_sessions_between(
        self, user_id: UUID, start_date: datetime, end_date: datetime
    ) -> list[LaborSession]:
        """
        Retrieve all labor sessions for a user within a date range.

        Args:
            user_id: The ID of the user
            start_date: Start of the date range
            end_date: End of the date range

        Returns:
            List of labor sessions within the date range
        """
        stmt = (
            select(LaborSession)
            .options(selectinload(LaborSession.contractions))
            .where(
                labor_sessions.c.user_id == user_id,
                labor_sessions.c.start_time >= start_date,
                labor_sessions.c.start_time <= end_date,
            )
        )

        result = await self._session.execute(stmt)
        return list(result.scalars().all())
