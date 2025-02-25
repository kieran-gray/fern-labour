from collections.abc import Iterable

from dishka import Provider

from app.setup.ioc.di_providers.admin_application import AdminApplicationProvider
from app.setup.ioc.di_providers.common_infrastructure import CommonInfrastructureProvider
from app.setup.ioc.di_providers.common_settings import CommonSettingsProvider
from app.setup.ioc.di_providers.events_application import EventsApplicationProvider
from app.setup.ioc.di_providers.events_infrastructure import EventsInfrastructureProvider
from app.setup.ioc.di_providers.labour_application import LabourApplicationProvider
from app.setup.ioc.di_providers.labour_infrastructure import LabourInfrastructureProvider
from app.setup.ioc.di_providers.notifications_application import NotificationsApplicationProvider
from app.setup.ioc.di_providers.subscriptions_application import SubscriptionsApplicationProvider
from app.setup.ioc.di_providers.subscriptions_infrastructure import (
    SubscriptionsInfrastructureProvider,
)
from app.setup.ioc.di_providers.user_application import UserApplicationProvider
from app.setup.ioc.di_providers.user_infrastructure import UserInfrastructureProvider


def get_providers() -> Iterable[Provider]:
    return (
        AdminApplicationProvider(),
        CommonSettingsProvider(),
        CommonInfrastructureProvider(),
        EventsApplicationProvider(),
        EventsInfrastructureProvider(),
        LabourApplicationProvider(),
        LabourInfrastructureProvider(),
        SubscriptionsApplicationProvider(),
        SubscriptionsInfrastructureProvider(),
        NotificationsApplicationProvider(),
        UserApplicationProvider(),
        UserInfrastructureProvider(),
    )
