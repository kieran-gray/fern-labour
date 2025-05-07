from collections.abc import Iterable

from dishka import Provider

from src.setup.ioc.di_providers.admin.application import AdminApplicationProvider
from src.setup.ioc.di_providers.core.infrastructure import CommonInfrastructureProvider
from src.setup.ioc.di_providers.core.settings import CommonSettingsProvider
from src.setup.ioc.di_providers.events.infrastructure import EventsInfrastructureProvider
from src.setup.ioc.di_providers.invites.application import InvitesApplicationProvider
from src.setup.ioc.di_providers.labour.application import LabourApplicationProvider
from src.setup.ioc.di_providers.labour.infrastructure import LabourInfrastructureProvider
from src.setup.ioc.di_providers.labour_events.application import LabourEventsApplicationProvider
from src.setup.ioc.di_providers.payments.infrastructure import PaymentsInfrastructureProvider
from src.setup.ioc.di_providers.subscription.application import SubscriptionApplicationProvider
from src.setup.ioc.di_providers.subscription.infrastructure import (
    SubscriptionInfrastructureProvider,
)
from src.setup.ioc.di_providers.subscription_events.application import (
    SubscriptionEventsApplicationProvider,
)
from src.setup.ioc.di_providers.user.application import UserApplicationProvider
from src.setup.ioc.di_providers.user.infrastructure import UserInfrastructureProvider


def get_providers() -> Iterable[Provider]:
    return (
        AdminApplicationProvider(),
        CommonSettingsProvider(),
        CommonInfrastructureProvider(),
        LabourEventsApplicationProvider(),
        EventsInfrastructureProvider(),
        LabourApplicationProvider(),
        LabourInfrastructureProvider(),
        LabourEventsApplicationProvider(),
        PaymentsInfrastructureProvider(),
        InvitesApplicationProvider(),
        SubscriptionApplicationProvider(),
        SubscriptionInfrastructureProvider(),
        SubscriptionEventsApplicationProvider(),
        UserApplicationProvider(),
        UserInfrastructureProvider(),
    )
