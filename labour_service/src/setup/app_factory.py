__all__ = "create_app_with_container"

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sentry_sdk
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.api.exception_handler import (
    ExceptionHandler,
    ExceptionHeaderMapper,
    ExceptionMapper,
    ExceptionMessageProvider,
)
from src.api.routes.router_root import root_router
from src.core.infrastructure.persistence.initialize_mapping import map_all
from src.setup.ioc.ioc_registry import get_providers
from src.setup.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    map_all()
    yield None
    await app.state.dishka_container.close()  # noqa; app.state is the place where dishka_container lives


def create_dishka_container(settings: Settings) -> AsyncContainer:
    return make_async_container(*get_providers(), context={Settings: settings})


def create_app_with_container(settings: Settings) -> FastAPI:
    new_app = create_app(settings)
    async_container = create_dishka_container(settings)
    setup_dishka(async_container, new_app)
    return new_app


def initialise_sentry(settings: Settings) -> None:
    sentry_sdk.init(
        environment=settings.base.environment,
        dsn="https://2e8e095bfd691bcc7f238e080ee09d07@o4508898015838208.ingest.de.sentry.io/4508898110210128",
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )


def create_app(settings: Settings) -> FastAPI:
    initialise_sentry(settings=settings)
    new_app: FastAPI = FastAPI(
        title="Labour Service",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    configure_app(new_app, settings)
    return new_app


def configure_app(new_app: FastAPI, settings: Settings) -> None:
    new_app.include_router(root_router)
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.cors.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    exception_message_provider = ExceptionMessageProvider()
    exception_mapper = ExceptionMapper()
    exception_header_mapper = ExceptionHeaderMapper()
    exception_handler = ExceptionHandler(
        new_app, exception_message_provider, exception_mapper, exception_header_mapper
    )
    exception_handler.setup_handlers()
