from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.common.application.services.contact_service import ContactService
from app.notification.application.services.notification_service import NotificationService
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings


class AdminApplicationProvider(Provider):
    component = ComponentEnum.ADMIN
    scope = Scope.REQUEST

    @provide
    def get_contact_service(
        self,
        notification_service: Annotated[
            NotificationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> ContactService:
        return ContactService(
            notification_service=notification_service,
            contact_email=settings.notifications.email.support_email,
        )
