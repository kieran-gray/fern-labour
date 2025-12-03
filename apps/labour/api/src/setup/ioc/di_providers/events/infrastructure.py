from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from fern_labour_core.events.producer import EventProducer
from fern_labour_pub_sub.producer import PubSubEventProducer

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
