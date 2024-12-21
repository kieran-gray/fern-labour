from dishka import Provider, Scope, provide

from app.application.services.birthing_person_service import BirthingPersonService


class BirthingPersonApplicationProvider(Provider):
    birthing_person_service = provide(
        source=BirthingPersonService,
        scope=Scope.REQUEST,
    )
