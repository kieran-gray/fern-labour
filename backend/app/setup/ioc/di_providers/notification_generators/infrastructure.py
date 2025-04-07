from dishka import Provider, Scope, provide

from app.notification.application.template_engines.email_template_engine import EmailTemplateEngine
from app.notification.infrastructure.notifications.email.jinja2_email_generation_service import (
    Jinja2EmailGenerationService,
)
from app.setup.ioc.di_component_enum import ComponentEnum


class NotificationGeneratorsInfrastructureProvider(Provider):
    component = ComponentEnum.NOTIFICATION_GENERATORS
    scope = Scope.APP

    @provide
    def get_email_template_engine(self) -> EmailTemplateEngine:
        return Jinja2EmailGenerationService()
