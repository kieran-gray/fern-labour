from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_service import NotificationService
from app.application.services.contact_service import ContactService
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
        email_generation_service: Annotated[
            EmailGenerationService, FromComponent(ComponentEnum.NOTIFICATIONS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> ContactService:
        return ContactService(
            notification_service=notification_service,
            email_generation_service=email_generation_service,
            contact_email=settings.notifications.email.support_email,
        )
