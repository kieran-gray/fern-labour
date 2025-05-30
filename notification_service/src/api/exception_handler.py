import logging
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Final

import pydantic
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from fern_labour_core.exceptions.application import ApplicationError
from fern_labour_core.exceptions.domain import DomainError

from src.notification.application.exceptions import (
    CannotGenerateNotificationContent,
    UnauthorizedWebhookRequest,
)
from src.notification.domain.exceptions import (
    CannotResendNotification,
    InvalidNotificationId,
    InvalidNotificationStatus,
    NotificationNotFoundByExternalId,
    NotificationNotFoundById,
)
from src.user.domain.exceptions import UserNotFoundById
from src.user.infrastructure.auth.interfaces.exceptions import AuthorizationError, InvalidTokenError

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ExceptionSchema:
    description: str


@dataclass(frozen=True, slots=True)
class ExceptionSchemaRich:
    description: str
    details: list[dict[str, Any]] | None = None


class ExceptionHandler:
    _ERROR_MAPPING: Final[dict[type[Exception], int]] = MappingProxyType({
        pydantic.ValidationError: status.HTTP_400_BAD_REQUEST,
        DomainError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ApplicationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        AuthorizationError: status.HTTP_401_UNAUTHORIZED,
        InvalidTokenError: status.HTTP_401_UNAUTHORIZED,
        InvalidNotificationStatus: status.HTTP_400_BAD_REQUEST,
        InvalidNotificationId: status.HTTP_400_BAD_REQUEST,
        NotificationNotFoundById: status.HTTP_404_NOT_FOUND,
        NotificationNotFoundByExternalId: status.HTTP_404_NOT_FOUND,
        UserNotFoundById: status.HTTP_404_NOT_FOUND,
        UnauthorizedWebhookRequest: status.HTTP_403_FORBIDDEN,
        CannotGenerateNotificationContent: status.HTTP_400_BAD_REQUEST,
        CannotResendNotification: status.HTTP_400_BAD_REQUEST,
    })

    def __init__(self, app: FastAPI) -> None:
        self._app = app

    async def _handle(self, _: Request, exc: Exception) -> ORJSONResponse:
        status_code: int = self._ERROR_MAPPING.get(
            type(exc),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        message = str(exc) if status_code < 500 else "Internal server error."

        if status_code >= 500:
            log.error(
                "Exception '%s' occurred: '%s'.",
                type(exc).__name__,
                exc,
                exc_info=exc,
            )
        else:
            log.warning("Exception '%s' occurred: '%s'.", type(exc).__name__, exc)

        if isinstance(exc, pydantic.ValidationError):
            response: ExceptionSchema | ExceptionSchemaRich = ExceptionSchemaRich(
                message,
                jsonable_encoder(exc.errors()),
            )
        else:
            response = ExceptionSchema(message)

        return ORJSONResponse(
            status_code=status_code,
            content=response,
        )

    def setup_handlers(self) -> None:
        for exc_class in self._ERROR_MAPPING:
            self._app.add_exception_handler(exc_class, self._handle)
        self._app.add_exception_handler(Exception, self._handle)
