from sqlalchemy import Delete, Select, delete, exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq

from app.application.exceptions import GatewayError
from app.application.user.gateways.user import UserGatewayInterface
from app.domain.user.vo_user import UserId, Username
from app.infrastructure.user.persistence_sqla.user import User


class SqlaUserGateway(UserGatewayInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User) -> None:
        """
        :raises GatewayError:
        """
        try:
            self._session.add(user)
            await self._session.flush()

        except OSError as error:
            raise GatewayError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise GatewayError("Database query failed.") from error

    async def read_by_id(self, user_id: UserId) -> User | None:
        """
        :raises GatewayError:
        """
        select_stmt: Select = select(User).where(eq(User.id_, user_id))  # type: ignore

        try:
            user: User | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except OSError as error:
            raise GatewayError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise GatewayError("Database query failed.") from error

    async def delete_by_id(self, user_id: UserId) -> bool:
        """
        :raises GatewayError:
        """
        delete_stmt: Delete = delete(User).where(eq(User.id_, user_id))  # type: ignore

        try:
            result = await self._session.execute(delete_stmt)
            return result.rowcount == 1

        except OSError as error:
            raise GatewayError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise GatewayError("Database query failed.") from error

    async def read_by_username(
        self, username: Username, for_update: bool = False
    ) -> User | None:
        """
        :raises GatewayError:
        """
        select_stmt: Select[tuple[User]] = select(User).where(
            eq(User.username, username),  # type: ignore
        )

        if for_update:
            select_stmt = select_stmt.with_for_update()

        try:
            user: User | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except OSError as error:
            raise GatewayError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise GatewayError("Database query failed.") from error

    async def is_username_unique(self, username: Username) -> bool:
        """
        :raises GatewayError:
        """
        select_exists_stmt: Select[tuple[bool]] = select(
            exists().where(eq(User.username, username)),  # type: ignore
        )

        try:
            username_exists: bool = (
                await self._session.scalar(select_exists_stmt) or False
            )

            return not username_exists

        except OSError as error:
            raise GatewayError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise GatewayError("Database query failed.") from error

    async def read_all(self, limit: int, offset: int) -> list[User]:
        """
        :raises GatewayError:
        """
        select_stmt: Select[tuple[User]] = (
            select(User).limit(limit).offset(offset)
        )

        try:
            users: list[User] = list(
                (await self._session.scalars(select_stmt)).all()
            )

            return users

        except OSError as error:
            raise GatewayError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise GatewayError("Database query failed.") from error
