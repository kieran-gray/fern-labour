import logging
from typing import NewType

from dishka import Provider, Scope, from_context, provide
from dishka.dependency_source.composite import CompositeDependencySource

from src.setup.ioc.di_component_enum import ComponentEnum
from src.setup.settings import Settings, SqlaEngineSettings

PostgresDsn = NewType("PostgresDsn", str)

log = logging.getLogger(__name__)


class CoreSettingsProvider(Provider):
    component = ComponentEnum.DEFAULT

    settings: CompositeDependencySource = from_context(provides=Settings, scope=Scope.RUNTIME)

    @provide(scope=Scope.APP)
    def provide_postgres_dsn(self, settings: Settings) -> PostgresDsn:
        return PostgresDsn(settings.db.postgres.dsn)

    @provide(scope=Scope.APP)
    def provide_sqla_engine_settings(self, settings: Settings) -> SqlaEngineSettings:
        return settings.db.sqla_engine
