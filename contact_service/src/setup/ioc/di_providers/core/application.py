from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.events.producer import EventProducer

from src.application.alert_service import AlertService
from src.application.contact_message_query_service import ContactMessageQueryService
from src.application.contact_message_service import ContactMessageService
from src.application.event_handlers.contact_message_created_event_handler import (
    ContactMessageCreatedEventHandler,
)
from src.domain.repository import ContactMessageRepository
from src.infrastructure.log_alert_service import LogAlertService
from src.infrastructure.slack.slack_alert_service import SlackAlertService
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings


class CoreApplicationProvider(Provider):
    component = ComponentEnum.DEFAULT
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def get_alert_service(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> AlertService:
        if settings.slack.slack_enabled:
            return SlackAlertService(
                token=settings.slack.token, channel=settings.slack.alert_channel
            )
        return LogAlertService()

    @provide
    def get_contact_service(
        self,
        contact_message_repository: Annotated[
            ContactMessageRepository, FromComponent(ComponentEnum.DEFAULT)
        ],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        alert_service: Annotated[AlertService, FromComponent(ComponentEnum.DEFAULT)],
    ) -> ContactMessageService:
        return ContactMessageService(
            contact_message_repository=contact_message_repository,
            event_producer=event_producer,
            alert_service=alert_service,
        )

    @provide
    def get_contact_query_service(
        self,
        contact_message_repository: Annotated[
            ContactMessageRepository, FromComponent(ComponentEnum.DEFAULT)
        ],
    ) -> ContactMessageQueryService:
        return ContactMessageQueryService(contact_message_repository=contact_message_repository)

    @provide
    def get_contact_message_created_event_handler(
        self,
        contact_message_query_service: Annotated[
            ContactMessageQueryService, FromComponent(ComponentEnum.DEFAULT)
        ],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> ContactMessageCreatedEventHandler:
        return ContactMessageCreatedEventHandler(
            contact_message_query_service=contact_message_query_service,
            event_producer=event_producer,
            contact_email=settings.base.support_email,
        )
