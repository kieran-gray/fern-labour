import logging
from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.notification.repository import NotificationRepository
from app.infrastructure.persistence.repositories.notification_repository import (
    SQLAlchemyNotificationRepository,
)
from app.setup.ioc.di_component_enum import ComponentEnum

log = logging.getLogger(__name__)


class NotificationsInfrastructureProvider(Provider):
    component = ComponentEnum.NOTIFICATIONS
    scope = Scope.REQUEST

    @provide
    def provide_notification_repository(
        self, async_session: Annotated[AsyncSession, FromComponent(ComponentEnum.DEFAULT)]
    ) -> NotificationRepository:
        return SQLAlchemyNotificationRepository(session=async_session)
