from collections.abc import Iterable

from dishka import Provider

from src.setup.ioc.di_providers.admin.application import AdminApplicationProvider
from src.setup.ioc.di_providers.common.infrastructure import CommonInfrastructureProvider
from src.setup.ioc.di_providers.common.settings import CommonSettingsProvider
from src.setup.ioc.di_providers.events.infrastructure import EventsInfrastructureProvider
from src.setup.ioc.di_providers.invites.application import InvitesApplicationProvider
from src.setup.ioc.di_providers.labour.application import LabourApplicationProvider
from src.setup.ioc.di_providers.labour.infrastructure import LabourInfrastructureProvider
from src.setup.ioc.di_providers.labour_events.application import LabourEventsApplicationProvider
from src.setup.ioc.di_providers.payment_events.application import PaymentEventsApplicationProvider
from src.setup.ioc.di_providers.payments.infrastructure import PaymentsInfrastructureProvider
from src.setup.ioc.di_providers.subscriptions.application import SubscriptionsApplicationProvider
from src.setup.ioc.di_providers.subscriptions.infrastructure import (
    SubscriptionsInfrastructureProvider,
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
        PaymentEventsApplicationProvider(),
        InvitesApplicationProvider(),
        SubscriptionsApplicationProvider(),
        SubscriptionsInfrastructureProvider(),
        UserApplicationProvider(),
        UserInfrastructureProvider(),
    )
