from collections.abc import Iterable

from dishka import Provider

from app.setup.ioc.di_providers.admin.application import AdminApplicationProvider
from app.setup.ioc.di_providers.common.infrastructure import CommonInfrastructureProvider
from app.setup.ioc.di_providers.common.settings import CommonSettingsProvider
from app.setup.ioc.di_providers.events.infrastructure import EventsInfrastructureProvider
from app.setup.ioc.di_providers.invites.application import InvitesApplicationProvider
from app.setup.ioc.di_providers.labour.application import LabourApplicationProvider
from app.setup.ioc.di_providers.labour.infrastructure import LabourInfrastructureProvider
from app.setup.ioc.di_providers.labour_events.application import LabourEventsApplicationProvider
from app.setup.ioc.di_providers.notification_generators.infrastructure import (
    NotificationGeneratorsInfrastructureProvider,
)
from app.setup.ioc.di_providers.notifications.application import NotificationsApplicationProvider
from app.setup.ioc.di_providers.notifications.infrastructure import (
    NotificationsInfrastructureProvider,
)
from app.setup.ioc.di_providers.payment_events.application import PaymentEventsApplicationProvider
from app.setup.ioc.di_providers.payments.infrastructure import PaymentsInfrastructureProvider
from app.setup.ioc.di_providers.subscriptions.application import SubscriptionsApplicationProvider
from app.setup.ioc.di_providers.subscriptions.infrastructure import (
    SubscriptionsInfrastructureProvider,
)
from app.setup.ioc.di_providers.user.application import UserApplicationProvider
from app.setup.ioc.di_providers.user.infrastructure import UserInfrastructureProvider


def get_providers() -> Iterable[Provider]:
    return (
        AdminApplicationProvider(),
        CommonSettingsProvider(),
        CommonInfrastructureProvider(),
        LabourEventsApplicationProvider(),
        EventsInfrastructureProvider(),
        LabourApplicationProvider(),
        LabourInfrastructureProvider(),
        PaymentsInfrastructureProvider(),
        PaymentEventsApplicationProvider(),
        InvitesApplicationProvider(),
        SubscriptionsApplicationProvider(),
        SubscriptionsInfrastructureProvider(),
        NotificationsApplicationProvider(),
        NotificationsInfrastructureProvider(),
        NotificationGeneratorsInfrastructureProvider(),
        UserApplicationProvider(),
        UserInfrastructureProvider(),
    )
