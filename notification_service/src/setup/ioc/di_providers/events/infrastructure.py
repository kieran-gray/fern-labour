from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from gcp_pub_sub_dishka.consumer import PubSubEventConsumer
from gcp_pub_sub_dishka.event_handler import TopicHandler
from gcp_pub_sub_dishka.producer import PubSubEventProducer

from src.core.domain.producer import EventProducer
from src.core.infrastructure.events.interfaces.consumer import EventConsumer
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
    def get_gcp_pub_sub_event_producer(self, settings: GCPSettings) -> EventProducer:
        return PubSubEventProducer(project_id=settings.project_id, retries=settings.retries)

    @provide
    def get_gcp_pub_sub_event_consumer(self, settings: GCPSettings) -> EventConsumer:
        topic_handlers = [
            TopicHandler(topic, handler, ComponentEnum.NOTIFICATION_EVENTS)
            for topic, handler in NOTIFICATION_EVENT_HANDLER_MAPPING.items()
        ]
        return PubSubEventConsumer(project_id=settings.project_id, topic_handlers=topic_handlers)
