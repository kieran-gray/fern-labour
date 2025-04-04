from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.labour.domain.labour.entity import Labour
from app.labour.domain.labour.enums import LabourPhase
from app.labour.domain.labour.repository import LabourRepository
from app.labour.domain.labour.value_objects.labour_id import LabourId
from app.labour.infrastructure.persistence.tables.labours import labours_table
from app.user.domain.value_objects.user_id import UserId


class SQLAlchemyLabourRepository(LabourRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, labour: Labour) -> None:
        """
        Save or update a labour.

        Args:
            labour: The labour to save
        """
        self._session.add(labour)
        await self._session.commit()

    async def delete(self, labour: Labour) -> None:
        """
        Delete a labour.

        Args:
            labour: The labour to delete
        """
        await self._session.delete(labour)
        await self._session.commit()

    async def get_by_id(self, labour_id: LabourId) -> Labour | None:
        """
        Retrieve a labour by its ID.

        Args:
            labour_id: The ID of the labour to retrieve

        Returns:
            The labour if found, None otherwise
        """
        stmt = select(Labour).where(labours_table.c.id == labour_id.value)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_labours_by_birthing_person_id(self, birthing_person_id: UserId) -> list[Labour]:
        """
        Retrieve an labours by Birthing Person ID.

        Args:
            birthing_person_id: The Birthing Person ID to retrieve labours for

        Returns:
            List of labours
        """
        stmt = select(Labour).where(labours_table.c.birthing_person_id == birthing_person_id.value)

        result = await self._session.execute(stmt)
        return list(result.scalars())

    async def get_active_labour_by_birthing_person_id(
        self, birthing_person_id: UserId
    ) -> Labour | None:
        """
        Retrieve an active labour by Birthing Person ID.

        Args:
            birthing_person_id: The Birthing Person ID to retrieve the labour for

        Returns:
            The labour if found, None otherwise
        """
        stmt = select(Labour).where(
            and_(
                labours_table.c.birthing_person_id == birthing_person_id.value,
                labours_table.c.current_phase != LabourPhase.COMPLETE,
            )
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
