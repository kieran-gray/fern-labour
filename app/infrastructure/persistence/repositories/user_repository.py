from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.infrastructure.persistence.tables.user import users_table


class SQLAlchemyUserRepository(BirthingPersonRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: BirthingPerson) -> None:
        """
        Save or update a user.

        Args:
            user: The user to save
        """
        self._session.add(user)
        await self._session.commit()

    async def delete(self, user: BirthingPerson) -> None:
        """
        Delete a user.

        Args:
            user: The user to delete
        """

        self._session.delete(user)
        await self._session.commit()

    async def get_by_id(self, user_id: UUID) -> BirthingPerson | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        stmt = select(BirthingPerson).where(users_table.c.id == user_id)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> BirthingPerson | None:
        """
        Retrieve a user by their email address.

        Args:
            email: The email address to look up

        Returns:
            The user if found, None otherwise
        """

        stmt = select(BirthingPerson).where(users_table.c.username == email)

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        """
        Check if a user exists with the given email.

        Args:
            email: The email address to check

        Returns:
            True if a user exists with this email, False otherwise
        """
        user = await self.get_by_email(email)
        return user is not None
