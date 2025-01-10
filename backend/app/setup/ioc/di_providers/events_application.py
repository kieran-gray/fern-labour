from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.events.event_handlers.labour_announcement_made_event_handler import (
    LabourAnnouncementMadeEventHandler,
)
from app.application.events.event_handlers.labour_begun_event_handler import LabourBegunEventHandler
from app.application.events.event_handlers.labour_completed_event_handler import (
    LabourCompletedEventHandler,
)
from app.application.events.event_handlers.subscriber_subscribed_to_event_handler import (
    SubscriberSubscribedToEventHandler,
)
from app.application.events.event_handlers.subscriber_unsubscribed_from_event_handler import (
    SubscriberUnsubscribedFromEventHandler,
)
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notfication_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
)
from app.application.notifications.notification_service import NotificationService
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.subscriber_service import SubscriberService
from app.domain.birthing_person.repository import BirthingPersonRepository
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
from app.setup.settings import Settings


class EventsApplicationProvider(Provider):
    component = ComponentEnum.EVENTS
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def get_email_notification_gateway(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> EmailNotificationGateway:
        if settings.notifications.email.emails_enabled:
            assert settings.notifications.email.smtp_host
            assert settings.notifications.email.emails_from_email
            assert settings.notifications.email.smtp_port
            return SMTPEmailNotificationGateway(
                smtp_host=settings.notifications.email.smtp_host,
                smtp_user=settings.notifications.email.smtp_user,
                smtp_password=settings.notifications.email.smtp_password,
                emails_from_email=settings.notifications.email.emails_from_email,
                emails_from_name=settings.notifications.email.emails_from_name,
                smtp_tls=settings.notifications.email.smtp_tls,
                smtp_ssl=settings.notifications.email.smtp_ssl,
                smtp_port=settings.notifications.email.smtp_port,
            )
        else:
            return LoggerEmailNotificationGateway()

    @provide(scope=Scope.APP)
    def get_sms_notification_gateway(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> SMSNotificationGateway:
        if settings.notifications.twilio.twilio_enabled:
            assert settings.notifications.twilio.account_sid
            assert settings.notifications.twilio.auth_token
            assert settings.notifications.twilio.sms_from_number
            return TwilioSMSNotificationGateway(
                account_sid=settings.notifications.twilio.account_sid,
                auth_token=settings.notifications.twilio.auth_token,
                sms_from_number=settings.notifications.twilio.sms_from_number,
            )
        else:
            return LoggerSMSNotificationGateway()

    @provide
    def get_notification_service(
        self,
        email_notification_gateway: EmailNotificationGateway,
        sms_notification_gateway: SMSNotificationGateway,
    ) -> NotificationService:
        return NotificationService(
            email_notification_gateway=email_notification_gateway,
            sms_notification_gateway=sms_notification_gateway,
        )

    @provide
    def get_email_generation_service(self) -> EmailGenerationService:
        return Jinja2EmailGenerationService()

    @provide
    def get_labour_announcement_made_event_handler(
        self,
        birthing_person_service: Annotated[
            BirthingPersonService, FromComponent(ComponentEnum.LABOUR)
        ],
        subscriber_service: Annotated[SubscriberService, FromComponent(ComponentEnum.SUBSCRIBER)],
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
    ) -> LabourAnnouncementMadeEventHandler:
        return LabourAnnouncementMadeEventHandler(
            birthing_person_service=birthing_person_service,
            subscriber_service=subscriber_service,
            notification_service=notification_service,
            email_generation_service=email_generation_service,
        )

    @provide
    def get_labour_begun_event_handler(
        self,
        birthing_person_service: Annotated[
            BirthingPersonService, FromComponent(ComponentEnum.LABOUR)
        ],
        subscriber_service: Annotated[SubscriberService, FromComponent(ComponentEnum.SUBSCRIBER)],
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
    ) -> LabourBegunEventHandler:
        return LabourBegunEventHandler(
            birthing_person_service=birthing_person_service,
            subscriber_service=subscriber_service,
            notification_service=notification_service,
            email_generation_service=email_generation_service,
        )

    @provide
    def get_labour_completed_event_handler(
        self,
        birthing_person_service: Annotated[
            BirthingPersonService, FromComponent(ComponentEnum.LABOUR)
        ],
        subscriber_service: Annotated[SubscriberService, FromComponent(ComponentEnum.SUBSCRIBER)],
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
    ) -> LabourCompletedEventHandler:
        return LabourCompletedEventHandler(
            birthing_person_service=birthing_person_service,
            subscriber_service=subscriber_service,
            notification_service=notification_service,
            email_generation_service=email_generation_service,
        )

    @provide
    def get_subscriber_subscribed_to_event_handler(
        self,
        birthing_person_repository: Annotated[
            BirthingPersonRepository, FromComponent(ComponentEnum.LABOUR)
        ],
    ) -> SubscriberSubscribedToEventHandler:
        return SubscriberSubscribedToEventHandler(
            birthing_person_repository=birthing_person_repository
        )

    @provide
    def get_subscriber_unsubscribed_from_event_handler(
        self,
        birthing_person_repository: Annotated[
            BirthingPersonRepository, FromComponent(ComponentEnum.LABOUR)
        ],
    ) -> SubscriberUnsubscribedFromEventHandler:
        return SubscriberUnsubscribedFromEventHandler(
            birthing_person_repository=birthing_person_repository
        )
