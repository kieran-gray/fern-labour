from collections.abc import Iterable

from dishka import Provider

from app.setup.ioc.di_providers.application_user import UserApplicationProvider
from app.setup.ioc.di_providers.infrastructure import InfrastructureProvider
from app.setup.ioc.di_providers.infrastructure_user import (
    UserAdaptersProvider,
    UserGatewaysProvider,
)
from app.setup.ioc.di_providers.presentation_user import (
    UserPresentationProvider,
)
from app.setup.ioc.di_providers.settings import SettingsProvider


def get_providers() -> Iterable[Provider]:
    infrastructure = (InfrastructureProvider(),)
    application_user = (UserApplicationProvider(),)
    infrastructure_user = (
        UserGatewaysProvider(),
        UserAdaptersProvider(),
    )
    presentation_user = (UserPresentationProvider(),)
    settings = (SettingsProvider(),)

    return (
        *infrastructure,
        *application_user,
        *infrastructure_user,
        *presentation_user,
        *settings,
    )
