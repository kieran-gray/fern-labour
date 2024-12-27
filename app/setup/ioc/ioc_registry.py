from collections.abc import Iterable

from dishka import Provider

from app.setup.ioc.di_providers.common_infrastructure import CommonInfrastructureProvider
from app.setup.ioc.di_providers.common_presentation import CommonPresentationProvider
from app.setup.ioc.di_providers.common_settings import CommonSettingsProvider
from app.setup.ioc.di_providers.events_application import EventsApplicationProvider
from app.setup.ioc.di_providers.events_infrastructure import EventsInfrastructureProvider
from app.setup.ioc.di_providers.labour_application import LabourApplicationProvider
from app.setup.ioc.di_providers.labour_infrastructure import LabourInfrastructureProvider
from app.setup.ioc.di_providers.subscriber_application import SubscriberApplicationProvider
from app.setup.ioc.di_providers.subscriber_infrastructure import SubscriberInfrastructureProvider


def get_providers() -> Iterable[Provider]:
    return (
        CommonInfrastructureProvider(),
        CommonSettingsProvider(),
        CommonPresentationProvider(),
        EventsApplicationProvider(),
        EventsInfrastructureProvider(),
        LabourApplicationProvider(),
        LabourInfrastructureProvider(),
        SubscriberApplicationProvider(),
        SubscriberInfrastructureProvider(),
    )
