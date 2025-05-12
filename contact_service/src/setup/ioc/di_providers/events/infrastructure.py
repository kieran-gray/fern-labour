from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.events.consumer import EventConsumer
from fern_labour_core.events.producer import EventProducer
from fern_labour_pub_sub.consumer import PubSubEventConsumer
from fern_labour_pub_sub.enums import ConsumerMode
from fern_labour_pub_sub.producer import PubSubEventProducer
from fern_labour_pub_sub.topic_handler import TopicHandler

from src.application.event_handlers.mapping import CONTACT_EVENT_HANDLER_MAPPING
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
            TopicHandler(topic, event_handler, ComponentEnum.DEFAULT)
            for topic, event_handler in CONTACT_EVENT_HANDLER_MAPPING.items()
        ]
        return PubSubEventConsumer(
            project_id=settings.project_id,
            topic_handlers=topic_handlers,
            mode=ConsumerMode(settings.consumer_mode),
            batch_max_messages=settings.max_batch_size,
        )
