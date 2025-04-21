from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from gcp_pub_sub_dishka.consumer import PubSubEventConsumer
from gcp_pub_sub_dishka.producer import PubSubEventProducer

from app.common.domain.producer import EventProducer
from app.common.infrastructure.events.interfaces.consumer import EventConsumer
from app.labour.application.event_handlers.mapping import LABOUR_EVENT_HANDLER_MAPPING
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import GCPSettings, Settings


class EventsInfrastructureProvider(Provider):
    component = ComponentEnum.EVENTS
    scope = Scope.APP

    @provide
    def get_gcp_settings(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> GCPSettings:
        return settings.events.gcp

    @provide
    def get_gcp_pub_sub_event_producer(self, settings: GCPSettings) -> EventProducer:
        return PubSubEventProducer(project_id=settings.project_id, retries=settings.retries)

    @provide
    def get_gcp_pub_sub_event_consumer(self, settings: GCPSettings) -> EventConsumer:
        return PubSubEventConsumer(
            project_id=settings.project_id, topic_handlers=LABOUR_EVENT_HANDLER_MAPPING
        )
