from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from src.common.domain.producer import EventProducer
from src.common.infrastructure.events.gcp_pub_sub.gcp_pub_sub_event_consumer import (
    PubSubEventConsumer,
)
from src.common.infrastructure.events.gcp_pub_sub.gcp_pub_sub_event_producer import (
    PubSubEventProducer,
)
from src.common.infrastructure.events.interfaces.consumer import EventConsumer
from src.notification.application.event_handlers.mapping import NOTIFICATION_EVENT_HANDLER_MAPPING
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import GCPSettings, Settings


class EventsInfrastructureProvider(Provider):
    component = ComponentEnum.EVENTS
    scope = Scope.APP

    @provide
    def get_gcp_settings(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> GCPSettings:
        return settings.events.gcp

    @provide
    def get_kafka_event_producer(self, settings: GCPSettings) -> EventProducer:
        return PubSubEventProducer(project_id=settings.project_id, retries=settings.retries)

    @provide
    def get_kafka_event_consumer(self, settings: GCPSettings) -> EventConsumer:
        return PubSubEventConsumer(
            project_id=settings.project_id, topic_handlers=NOTIFICATION_EVENT_HANDLER_MAPPING
        )
