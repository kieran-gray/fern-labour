from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.common.application.services.contact_service import ContactService
from app.notification.application.services.notification_service import NotificationService
from app.notification.application.template_engines.email_template_engine import EmailTemplateEngine
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
        email_template_engine: Annotated[
            EmailTemplateEngine, FromComponent(ComponentEnum.NOTIFICATION_GENERATORS)
        ],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> ContactService:
        return ContactService(
            notification_service=notification_service,
            email_template_engine=email_template_engine,
            contact_email=settings.notifications.email.support_email,
        )
