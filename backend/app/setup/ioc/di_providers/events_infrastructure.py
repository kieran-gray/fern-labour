from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from app.application.events.consumer import EventConsumer
from app.application.events.producer import EventProducer
from app.infrastructure.events.kafka_event_consumer import KafkaEventConsumer
from app.infrastructure.events.kafka_event_producer import KafkaEventProducer
from app.setup.ioc.di_component_enum import ComponentEnum
from app.setup.settings import Settings


class EventsInfrastructureProvider(Provider):
    component = ComponentEnum.EVENTS
    scope = Scope.APP

    @provide
    def get_kafka_event_producer(
        self, settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)]
    ) -> EventProducer:
        return KafkaEventProducer(
            bootstrap_servers=settings.events.kafka.bootstrap_servers,
            acks=settings.events.kafka_producer.acks,
            retries=settings.events.kafka_producer.retries,
            topic_prefix=settings.events.kafka.topic_prefix,
        )

    @provide
    def get_kafka_event_consumer(
        self,
        settings: Annotated[Settings, FromComponent(ComponentEnum.DEFAULT)],
    ) -> EventConsumer:
        return KafkaEventConsumer(
            bootstrap_servers=settings.events.kafka.bootstrap_servers,
            group_id=settings.events.kafka_consumer.group_id,
            topic_prefix=settings.events.kafka.topic_prefix,
        )
