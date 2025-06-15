from collections.abc import Iterable

from dishka import Provider

from src.setup.ioc.di_providers.common.application import CommonApplicationProvider
from src.setup.ioc.di_providers.common.infrastructure import CommonInfrastructureProvider
from src.setup.ioc.di_providers.common.settings import CommonSettingsProvider
from src.setup.ioc.di_providers.events.infrastructure import EventsInfrastructureProvider
from src.setup.ioc.di_providers.notification_events.application import (
    NotificationEventsApplicationProvider,
)
from src.setup.ioc.di_providers.notifications.application import NotificationsApplicationProvider
from src.setup.ioc.di_providers.notifications.infrastructure import (
    NotificationsInfrastructureProvider,
)
from src.setup.ioc.di_providers.user.application import UserApplicationProvider
from src.setup.ioc.di_providers.user.infrastructure import UserInfrastructureProvider


def get_providers() -> Iterable[Provider]:
    return (
        CommonApplicationProvider(),
        CommonSettingsProvider(),
        CommonInfrastructureProvider(),
        EventsInfrastructureProvider(),
        NotificationsApplicationProvider(),
        NotificationsInfrastructureProvider(),
        NotificationEventsApplicationProvider(),
        UserApplicationProvider(),
        UserInfrastructureProvider(),
    )
