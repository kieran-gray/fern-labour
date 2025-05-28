from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.events.producer import EventProducer

from src.notification.application.interfaces.notification_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
    WhatsAppNotificationGateway,
)
from src.notification.application.services.notification_delivery_service import (
    NotificationDeliveryService,
)
from src.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from src.notification.application.services.notification_router import NotificationRouter
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.enums import NotificationChannel
from src.notification.domain.repository import NotificationRepository
from src.notification.infrastructure.gateways.log_gateway import (
    LogNotificationGateway,
)
from src.notification.infrastructure.gateways.smtp_email_gateway import (
    SMTPEmailNotificationGateway,
)
from src.notification.infrastructure.gateways.twilio_sms_gateway import (
    TwilioSMSNotificationGateway,
)
from src.notification.infrastructure.gateways.twilio_whatsapp_gateway import (
    TwilioWhatsAppNotificationGateway,
)
from src.notification.infrastructure.security.request_verification_service import (
    RequestVerificationService,
)
from src.notification.infrastructure.template_engines.jinja2_email_template_engine import (
    Jinja2EmailTemplateEngine,
)
from src.notification.infrastructure.template_engines.sms_template_engine import SMSTemplateEngine
from src.notification.infrastructure.template_engines.whatsapp_template_engine import (
    WhatsAppTemplateEngine,
)
from src.notification.infrastructure.twilio.twilio_request_verification_service import (
    TwilioRequestVerificationService,
)
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import EmailSettings, Settings, TwilioSettings


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
                smtp_port=settings.smtp_port,
                emails_from_email=settings.emails_from_email,
                smtp_tls=settings.smtp_tls,
                smtp_ssl=settings.smtp_ssl,
                smtp_user=settings.smtp_user,
                smtp_password=settings.smtp_password,
                emails_from_name=settings.emails_from_name,
            )
        else:
            return LogNotificationGateway()

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
            return LogNotificationGateway()

    @provide(scope=Scope.APP)
    def get_whatsapp_notification_gateway(
        self, settings: TwilioSettings
    ) -> WhatsAppNotificationGateway:
        if settings.twilio_enabled:
            assert settings.account_sid
            assert settings.auth_token
            return TwilioWhatsAppNotificationGateway(
                account_sid=settings.account_sid,
                auth_token=settings.auth_token,
                messaging_service_sid=settings.messaging_service_sid,
            )
        else:
            return LogNotificationGateway()

    @provide(scope=Scope.APP)
    def get_notification_router(
        self,
        email_notification_gateway: EmailNotificationGateway,
        sms_notification_gateway: SMSNotificationGateway,
        whatsapp_notification_gateway: WhatsAppNotificationGateway,
    ) -> NotificationRouter:
        router = NotificationRouter()
        router.register_gateway(
            channel=NotificationChannel.EMAIL.value, gateway=email_notification_gateway
        )
        router.register_gateway(
            channel=NotificationChannel.SMS.value, gateway=sms_notification_gateway
        )
        router.register_gateway(
            channel=NotificationChannel.WHATSAPP, gateway=whatsapp_notification_gateway
        )
        return router

    @provide(scope=Scope.APP)
    def provide_request_verification_service(
        self, settings: TwilioSettings
    ) -> RequestVerificationService:
        return TwilioRequestVerificationService(auth_token=settings.auth_token or "")

    @provide
    def get_notification_generation_service(
        self,
        notification_repository: NotificationRepository,
    ) -> NotificationGenerationService:
        notification_generation_service = NotificationGenerationService(
            notification_repo=notification_repository
        )
        notification_generation_service.register_template_engine(
            channel=NotificationChannel.EMAIL, template_engine=Jinja2EmailTemplateEngine()
        )
        notification_generation_service.register_template_engine(
            channel=NotificationChannel.SMS, template_engine=SMSTemplateEngine()
        )
        notification_generation_service.register_template_engine(
            channel=NotificationChannel.WHATSAPP, template_engine=WhatsAppTemplateEngine()
        )
        return notification_generation_service

    @provide
    def get_notification_service(
        self,
        notification_router: NotificationRouter,
        notification_generation_service: NotificationGenerationService,
        notification_repository: NotificationRepository,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> NotificationService:
        return NotificationService(
            notification_router=notification_router,
            notification_generation_service=notification_generation_service,
            notification_repository=notification_repository,
            event_producer=event_producer,
        )

    @provide
    def get_notification_delivery_service(
        self,
        notification_service: NotificationService,
        notification_router: NotificationRouter,
        notification_repository: NotificationRepository,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
    ) -> NotificationDeliveryService:
        return NotificationDeliveryService(
            notification_service=notification_service,
            notification_router=notification_router,
            notification_repository=notification_repository,
            event_producer=event_producer,
        )
