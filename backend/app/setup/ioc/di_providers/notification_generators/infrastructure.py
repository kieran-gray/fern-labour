from dishka import Provider, Scope, provide

from app.notification.application.services.email_generation_service import EmailGenerationService
from app.notification.infrastructure.notifications.email.jinja2_email_generation_service import (
    Jinja2EmailGenerationService,
)
from app.setup.ioc.di_component_enum import ComponentEnum


class NotificationGeneratorsInfrastructureProvider(Provider):
    component = ComponentEnum.NOTIFICATION_GENERATORS
    scope = Scope.APP

    @provide
    def get_email_generation_service(self) -> EmailGenerationService:
        return Jinja2EmailGenerationService()
