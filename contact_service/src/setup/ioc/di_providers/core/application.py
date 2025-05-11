from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.events.producer import EventProducer

from src.application.contact_message_service import ContactMessageService
from src.domain.repository import ContactMessageRepository
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings


class CoreApplicationProvider(Provider):
    component = ComponentEnum.DEFAULT
    scope = Scope.REQUEST

    @provide
    def get_contact_service(
        self,
        contact_message_repository: Annotated[
            ContactMessageRepository, FromComponent(ComponentEnum.DEFAULT)
        ],
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> ContactMessageService:
        return ContactMessageService(
            contact_message_repository=contact_message_repository,
            event_producer=event_producer,
            contact_email=settings.base.support_email,
        )
