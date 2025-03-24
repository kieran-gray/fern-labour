from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notfication_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
)
from app.application.notifications.notification_service import NotificationService
from app.domain.notification.repository import NotificationRepository
from app.infrastructure.notifications.email.jinja2_email_generation_service import (
    Jinja2EmailGenerationService,
)
from app.infrastructure.notifications.email.logger_email_notification_gateway import (
    LoggerEmailNotificationGateway,
)
from app.infrastructure.notifications.email.smtp_email_notification_gateway import (
    SMTPEmailNotificationGateway,
)
from app.infrastructure.notifications.sms.logger_sms_notification_gateway import (
    LoggerSMSNotificationGateway,
)
from app.infrastructure.notifications.sms.twilio_sms_notification_gateway import (
    TwilioSMSNotificationGateway,
)
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import EmailSettings, Settings, TwilioSettings


class NotificationsApplicationProvider(Provider):
    component = ComponentEnum.NOTIFICATIONS
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def get_email_settings(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> EmailSettings:
        return settings.notifications.email

    @provide(scope=Scope.APP)
    def get_twilio_settings(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> TwilioSettings:
        return settings.notifications.twilio

    @provide(scope=Scope.APP)
    def get_email_notification_gateway(self, settings: EmailSettings) -> EmailNotificationGateway:
        if settings.emails_enabled:
            assert settings.smtp_host
            assert settings.emails_from_email
            assert settings.smtp_port
            return SMTPEmailNotificationGateway(
                smtp_host=settings.smtp_host,
                smtp_user=settings.smtp_user,
                smtp_password=settings.smtp_password,
                emails_from_email=settings.emails_from_email,
                emails_from_name=settings.emails_from_name,
                smtp_tls=settings.smtp_tls,
                smtp_ssl=settings.smtp_ssl,
                smtp_port=settings.smtp_port,
            )
        else:
            return LoggerEmailNotificationGateway()

    @provide(scope=Scope.APP)
    def get_sms_notification_gateway(self, settings: TwilioSettings) -> SMSNotificationGateway:
        if settings.twilio_enabled:
            assert settings.account_sid
            assert settings.auth_token
            return TwilioSMSNotificationGateway(
                account_sid=settings.account_sid,
                auth_token=settings.auth_token,
                sms_from_number=settings.sms_from_number,
                messaging_service_sid=settings.messaging_service_sid,
            )
        else:
            return LoggerSMSNotificationGateway()

    @provide
    def get_notification_service(
        self,
        email_notification_gateway: EmailNotificationGateway,
        sms_notification_gateway: SMSNotificationGateway,
        notification_repository: NotificationRepository,
    ) -> NotificationService:
        return NotificationService(
            email_notification_gateway=email_notification_gateway,
            sms_notification_gateway=sms_notification_gateway,
            notification_repository=notification_repository,
        )

    @provide
    def get_email_generation_service(self) -> EmailGenerationService:
        return Jinja2EmailGenerationService()
