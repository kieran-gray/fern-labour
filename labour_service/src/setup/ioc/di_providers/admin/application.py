from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.admin.application.contact_service import ContactService
from src.core.domain.producer import EventProducer
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings


class AdminApplicationProvider(Provider):
    component = ComponentEnum.ADMIN
    scope = Scope.REQUEST

    @provide
    def get_contact_service(
        self,
        event_producer: Annotated[EventProducer, FromComponent(ComponentEnum.EVENTS)],
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> ContactService:
        return ContactService(
            event_producer=event_producer,
            contact_email=settings.base.support_email,
        )
