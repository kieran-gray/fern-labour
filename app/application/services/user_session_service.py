import logging
from datetime import datetime, timedelta

from app.application.adapters.session_timer import SessionTimer
from app.application.services.user_service import UserService
from app.domain.entities.user_session import UserSession
from app.domain.exceptions.user import UserNotFoundById
from app.domain.value_objects.user_id import UserId

log = logging.getLogger(__name__)


class UserSessionService:
    def __init__(self, session_timer: SessionTimer, user_service: UserService):
        self._session_timer = session_timer
        self._user_service = user_service

    async def create_user_session(self, user_id: UserId) -> UserSession:
        user = await self._user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundById(user_id)

        expiration: datetime = self._session_timer.access_expiration
        user_session = user.create_session(expiration=expiration)
        await self._user_service.save_user(user)

        return user_session

    async def delete_all_user_sessions(self, user_id: UserId) -> None:
        user = await self._user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundById(user_id)

        user.delete_all_sessions()
        await self._user_service.save_user(user)

    async def is_user_session_near_expiry(self, user_id: UserId) -> bool:
        user = await self._user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundById(user_id)

        time_remaining: timedelta = user.session.expiration - self._session_timer.current_time

        return time_remaining < self._session_timer.refresh_trigger_interval

    async def prolong_user_session(self, user_id: UserId) -> UserSession:
        user = await self._user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundById(user_id)

        new_expiration: datetime = self._session_timer.access_expiration
        user.session.expiration = new_expiration

        await self._user_service.save_user(user)
        return user.session
