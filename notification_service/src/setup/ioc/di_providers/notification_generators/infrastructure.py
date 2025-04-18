from dishka import Provider, Scope, provide

from src.notification.application.template_engines.email_template_engine import EmailTemplateEngine
from src.notification.application.template_engines.sms_template_engine import SMSTemplateEngine
from src.notification.infrastructure.notifications.email.jinja2_email_template_engine import (
    Jinja2EmailTemplateEngine,
)
from src.notification.infrastructure.notifications.sms.sms_template_engine import (
    SMSTemplateEngine as ConcreteSMSTemplateEngine,
)
from src.setup.ioc.di_component_enum import ComponentEnum


class NotificationGeneratorsInfrastructureProvider(Provider):
    component = ComponentEnum.NOTIFICATION_GENERATORS
    scope = Scope.APP

    @provide
    def get_email_template_engine(self) -> EmailTemplateEngine:
        return Jinja2EmailTemplateEngine()

    @provide
    def get_sms_template_engine(self) -> SMSTemplateEngine:
        return ConcreteSMSTemplateEngine()
