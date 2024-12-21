from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.infrastructure.persistence.tables.birthing_persons import birthing_persons_table


class SQLAlchemyBirthingPersonRepository(BirthingPersonRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, birthing_person: BirthingPerson) -> None:
        """
        Save or update a birthing person.

        Args:
            birthing_person: The birthing person to save
        """
        self._session.add(birthing_person)
        await self._session.commit()

    async def delete(self, birthing_person: BirthingPerson) -> None:
        """
        Delete a birthing person.

        Args:
            birthing_person: The birthing person to delete
        """

        self._session.delete(birthing_person)
        await self._session.commit()

    async def get_by_id(self, birthing_person_id: BirthingPersonId) -> BirthingPerson | None:
        """
        Retrieve a birthing person by their ID.

        Args:
            birthing_person_id: The ID of the birthing person to retrieve

        Returns:
            The birthing person if found, None otherwise
        """
        stmt = (
            select(BirthingPerson)
            .options(
                selectinload(BirthingPerson.contacts),
                selectinload(BirthingPerson.labours),
            )
            .where(birthing_persons_table.c.id == birthing_person_id.value)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
