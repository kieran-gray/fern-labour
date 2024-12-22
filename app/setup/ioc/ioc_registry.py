from collections.abc import Iterable

from dishka import Provider

from app.setup.ioc.di_providers.birthing_person.application import BirthingPersonApplicationProvider
from app.setup.ioc.di_providers.birthing_person.infrastructure import (
    BirthingPersonRepositoriesProvider,
)
from app.setup.ioc.di_providers.core.applicaton import NotificationGatewayProvider
from app.setup.ioc.di_providers.core.infrastructure import InfrastructureProvider
from app.setup.ioc.di_providers.core.presentation import PresentationProvider
from app.setup.ioc.di_providers.core.settings import SettingsProvider
from app.setup.ioc.di_providers.labour.application import LabourApplicationProvider
from app.setup.ioc.di_providers.labour.infrastructure import LabourRepositoriesProvider


def get_providers() -> Iterable[Provider]:
    application = (NotificationGatewayProvider(),)
    infrastructure = (InfrastructureProvider(),)
    presentation = (PresentationProvider(),)
    settings = (SettingsProvider(),)

    application_birthing_person = (BirthingPersonApplicationProvider(),)
    infrastructure_birthing_person = (BirthingPersonRepositoriesProvider(),)

    application_labour = (LabourApplicationProvider(),)
    infrastructure_labour = (LabourRepositoriesProvider(),)

    return (
        *application,
        *infrastructure,
        *presentation,
        *settings,
        *application_birthing_person,
        *infrastructure_birthing_person,
        *application_labour,
        *infrastructure_labour,
    )
