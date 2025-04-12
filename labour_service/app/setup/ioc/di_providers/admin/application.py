from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.common.application.services.contact_service import ContactService
from app.common.domain.producer import EventProducer
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings


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
