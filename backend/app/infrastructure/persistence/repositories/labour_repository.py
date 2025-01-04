from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.labour.entity import Labour
from app.domain.labour.repository import LabourRepository
from app.domain.labour.vo_labour_id import LabourId
from app.infrastructure.persistence.tables.labours import labours_table


class SQLAlchemyLabourRepository(LabourRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, labour: Labour) -> None:
        """
        Save or update a labor.

        Args:
            labour: The labor to save
        """
        self._session.add(labour)
        await self._session.commit()

    async def delete(self, labour: Labour) -> None:
        """
        Delete a labor.

        Args:
            labour: The labor to delete
        """
        await self._session.delete(labour)
        await self._session.commit()

    async def get_by_id(self, labour_id: LabourId) -> Labour | None:
        """
        Retrieve a labor by its ID.

        Args:
            labour_id: The ID of the labor to retrieve

        Returns:
            The labor if found, None otherwise
        """
        stmt = select(Labour).where(labours_table.c.id == labour_id.value)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
