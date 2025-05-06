from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.events.producer import EventProducer
from gcp_pub_sub_dishka.consumer import PubSubEventConsumer
from gcp_pub_sub_dishka.event_handler import TopicHandler
from gcp_pub_sub_dishka.producer import PubSubEventProducer

from fern_labour_core.events.consumer import EventConsumer
from src.labour.application.event_handlers.mapping import LABOUR_EVENT_HANDLER_MAPPING
from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import GCPSettings, Settings
from src.subscription.application.event_handlers.mapping import SUBSCRIPTION_EVENT_HANDLER_MAPPING


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
        topic_handlers = []
        for topic, event_handler in LABOUR_EVENT_HANDLER_MAPPING.items():
            topic_handlers.append(TopicHandler(topic, event_handler, ComponentEnum.LABOUR_EVENTS))

        for topic, event_handler in SUBSCRIPTION_EVENT_HANDLER_MAPPING.items():
            topic_handlers.append(
                TopicHandler(topic, event_handler, ComponentEnum.SUBSCRIPTION_EVENTS)
            )
        return PubSubEventConsumer(project_id=settings.project_id, topic_handlers=topic_handlers)
