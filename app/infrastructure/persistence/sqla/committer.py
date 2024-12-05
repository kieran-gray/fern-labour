from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.committer import CommitterInterface
from app.application.exceptions import GatewayError


class SqlaCommitter(CommitterInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        """
        :raises GatewayError:
        """
        try:
            await self._session.commit()

        except OSError as error:
            raise GatewayError("Connection failed, commit failed.") from error
        except SQLAlchemyError as error:
            raise GatewayError(
                "Database query failed, commit failed."
            ) from error
