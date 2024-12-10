from collections.abc import Iterable

from dishka import Provider

from app.core.ioc.di_providers.core.infrastructure import InfrastructureProvider
from app.core.ioc.di_providers.core.presentation import PresentationProvider
from app.core.ioc.di_providers.core.settings import SettingsProvider
from app.core.ioc.di_providers.labor_session.application import LaborSessionApplicationProvider
from app.core.ioc.di_providers.labor_session.infrastructure import LaborSessionRepositoriesProvider
from app.core.ioc.di_providers.user.application import UserApplicationProvider
from app.core.ioc.di_providers.user.infrastructure import (
    UserAdaptersProvider,
    UserRepositoriesProvider,
)


def get_providers() -> Iterable[Provider]:
    infrastructure = (InfrastructureProvider(),)
    presentation = (PresentationProvider(),)
    settings = (SettingsProvider(),)

    application_user = (UserApplicationProvider(),)
    infrastructure_user = (
        UserRepositoriesProvider(),
        UserAdaptersProvider(),
    )

    application_labor_session = (LaborSessionApplicationProvider(),)
    infrastructure_labor_session = (LaborSessionRepositoriesProvider(),)

    return (
        *infrastructure,
        *presentation,
        *settings,
        *application_user,
        *infrastructure_user,
        *application_labor_session,
        *infrastructure_labor_session,
    )
