from collections.abc import Iterable

from dishka import Provider

from src.setup.ioc.di_providers.core.application import CoreApplicationProvider
from src.setup.ioc.di_providers.core.infrastructure import CoreInfrastructureProvider
from src.setup.ioc.di_providers.core.settings import CoreSettingsProvider
from src.setup.ioc.di_providers.events.infrastructure import EventsInfrastructureProvider
from src.setup.ioc.di_providers.user.application import UserApplicationProvider
from src.setup.ioc.di_providers.user.infrastructure import UserInfrastructureProvider


def get_providers() -> Iterable[Provider]:
    return (
        CoreApplicationProvider(),
        CoreSettingsProvider(),
        CoreInfrastructureProvider(),
        EventsInfrastructureProvider(),
        UserApplicationProvider(),
        UserInfrastructureProvider(),
    )
