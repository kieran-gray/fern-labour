import logging
from datetime import datetime, timedelta

from app.application.committer import CommitterInterface
from app.application.user.gateways.session import SessionGatewayInterface
from app.application.user.ports.session_id_generator import (
    SessionIdGeneratorInterface,
)
from app.application.user.ports.session_timer import SessionTimerInterface
from app.application.user.record_session import SessionRecord
from app.domain.user.exceptions.non_existence import SessionNotFoundById
from app.domain.user.vo_user import UserId

log = logging.getLogger(__name__)


class SessionService:
    def __init__(
        self,
        session_id_generator: SessionIdGeneratorInterface,
        session_timer: SessionTimerInterface,
        session_gateway: SessionGatewayInterface,
        committer: CommitterInterface,
    ):
        self._session_id_generator = session_id_generator
        self._session_timer = session_timer
        self._session_gateway = session_gateway
        self._committer = committer

    async def create_session(self, user_id: UserId) -> SessionRecord:
        log.debug(f"Started. User id: '{user_id.value}'.")

        session_id: str = self._session_id_generator()
        expiration: datetime = self._session_timer.access_expiration
        session_record: SessionRecord = SessionRecord(
            id_=session_id,
            user_id=user_id,
            expiration=expiration,
        )

        log.debug(
            "Done. User id: '%s', Session id: '%s'.",
            user_id.value,
            session_record.id_,
        )
        return session_record

    async def save_session(self, session_record: SessionRecord) -> None:
        """
        :raises GatewayError:
        """
        log.debug(f"Started. Session id: '{session_record.id_}'.")

        await self._session_gateway.save(session_record)

        await self._committer.commit()
        log.debug(f"Done. Session id: '{session_record.id_}'.")

    async def delete_session(self, session_id: str) -> None:
        """
        :raises GatewayError:
        :raises SessionNotFoundById:
        """
        log.debug(
            f"Started. Session id: '{session_id}'.",
        )

        if not await self._session_gateway.delete(session_id):
            raise SessionNotFoundById(session_id)

        await self._committer.commit()
        log.debug(f"Done. Session id: '{session_id}'.")

    async def delete_all_sessions_by_user_id(self, user_id: UserId) -> None:
        """
        :raises GatewayError:
        """
        log.debug(f"Started. User id: '{user_id.value}'.")

        await self._session_gateway.delete_all_for_user(user_id)

        await self._committer.commit()
        log.debug(f"Done. User id: '{user_id.value}'.")

    def is_session_near_expiry(self, session: SessionRecord) -> bool:
        log.debug(f"Started. Session id: {session.id_}.")

        time_remaining: timedelta = (
            session.expiration - self._session_timer.current_time
        )

        log.debug(f"Done. Session id: {session.id_}.")
        return time_remaining < self._session_timer.refresh_trigger_interval

    async def prolong_session(self, session: SessionRecord) -> None:
        """
        :raises GatewayError:
        """
        log.debug(f"Started. Session id: {session.id_}.")

        new_expiration: datetime = self._session_timer.access_expiration
        session.expiration = new_expiration

        await self._session_gateway.save(session)

        await self._committer.commit()
        log.debug(f"Done. Session id: {session.id_}.")
