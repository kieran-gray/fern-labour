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

from src.labour.application.exceptions import (
    InvalidLabourUpdateRequest,
    LabourInviteRateLimitExceeded,
)
from src.labour.domain.contraction.exceptions import (
    CannotDeleteActiveContraction,
    CannotUpdateActiveContraction,
    ContractionIdInvalid,
    ContractionNotFoundById,
    ContractionsOverlappingAfterUpdate,
    ContractionStartTimeAfterEndTime,
)
from src.labour.domain.labour.exceptions import (
    CannotCompleteLabourWithActiveContraction,
    CannotDeleteActiveLabour,
    CannotSubscribeToOwnLabour,
    InvalidLabourId,
    InvalidLabourUpdateId,
    LabourAlreadyBegun,
    LabourAlreadyCompleted,
    LabourHasActiveContraction,
    LabourHasNoActiveContraction,
    LabourNotFoundById,
    LabourUpdateNotFoundById,
    UnauthorizedLabourRequest,
)
from src.labour.domain.labour_update.exceptions import TooSoonSinceLastAnnouncement
from src.payments.infrastructure.stripe.exceptions import (
    StripeProductNotFound,
    WebhookHasInvalidSignature,
)
from src.subscription.application.exceptions import SubscriberInviteRateLimitExceeded
from src.subscription.domain.exceptions import (
    SubscriberAlreadyRequested,
    SubscriberAlreadySubscribed,
    SubscriberIsBlocked,
    SubscriberIsNotBlocked,
    SubscriberIsRemoved,
    SubscriberNotSubscribed,
    SubscriptionAccessLevelInvalid,
    SubscriptionNotFoundById,
    SubscriptionTokenIncorrect,
    UnauthorizedSubscriptionRequest,
    UnauthorizedSubscriptionUpdateRequest,
)
from src.user.domain.exceptions import (
    UserDoesNotHaveActiveLabour,
    UserHasActiveLabour,
    UserNotFoundById,
)
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
    _ERROR_MAPPING: Final[MappingProxyType[type[Exception], int]] = MappingProxyType(
        {
            pydantic.ValidationError: status.HTTP_400_BAD_REQUEST,
            DomainError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            ApplicationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            UserNotFoundById: status.HTTP_404_NOT_FOUND,
            UserHasActiveLabour: status.HTTP_400_BAD_REQUEST,
            UserDoesNotHaveActiveLabour: status.HTTP_404_NOT_FOUND,
            LabourHasActiveContraction: status.HTTP_400_BAD_REQUEST,
            LabourHasNoActiveContraction: status.HTTP_400_BAD_REQUEST,
            LabourAlreadyCompleted: status.HTTP_400_BAD_REQUEST,
            LabourAlreadyBegun: status.HTTP_400_BAD_REQUEST,
            CannotCompleteLabourWithActiveContraction: status.HTTP_400_BAD_REQUEST,
            SubscriberAlreadySubscribed: status.HTTP_400_BAD_REQUEST,
            SubscriberNotSubscribed: status.HTTP_400_BAD_REQUEST,
            SubscriptionTokenIncorrect: status.HTTP_403_FORBIDDEN,
            CannotSubscribeToOwnLabour: status.HTTP_400_BAD_REQUEST,
            AuthorizationError: status.HTTP_401_UNAUTHORIZED,
            InvalidTokenError: status.HTTP_401_UNAUTHORIZED,
            TooSoonSinceLastAnnouncement: status.HTTP_400_BAD_REQUEST,
            SubscriberIsBlocked: status.HTTP_403_FORBIDDEN,
            SubscriptionNotFoundById: status.HTTP_404_NOT_FOUND,
            UnauthorizedSubscriptionRequest: status.HTTP_403_FORBIDDEN,
            UnauthorizedSubscriptionUpdateRequest: status.HTTP_403_FORBIDDEN,
            InvalidLabourId: status.HTTP_400_BAD_REQUEST,
            InvalidLabourUpdateId: status.HTTP_400_BAD_REQUEST,
            LabourUpdateNotFoundById: status.HTTP_404_NOT_FOUND,
            ContractionStartTimeAfterEndTime: status.HTTP_400_BAD_REQUEST,
            ContractionIdInvalid: status.HTTP_400_BAD_REQUEST,
            ContractionsOverlappingAfterUpdate: status.HTTP_400_BAD_REQUEST,
            ContractionNotFoundById: status.HTTP_404_NOT_FOUND,
            CannotUpdateActiveContraction: status.HTTP_400_BAD_REQUEST,
            UnauthorizedLabourRequest: status.HTTP_403_FORBIDDEN,
            CannotDeleteActiveLabour: status.HTTP_400_BAD_REQUEST,
            LabourNotFoundById: status.HTTP_404_NOT_FOUND,
            CannotDeleteActiveContraction: status.HTTP_400_BAD_REQUEST,
            StripeProductNotFound: status.HTTP_404_NOT_FOUND,
            LabourInviteRateLimitExceeded: status.HTTP_429_TOO_MANY_REQUESTS,
            SubscriberInviteRateLimitExceeded: status.HTTP_429_TOO_MANY_REQUESTS,
            SubscriberIsNotBlocked: status.HTTP_400_BAD_REQUEST,
            SubscriberIsRemoved: status.HTTP_400_BAD_REQUEST,
            SubscriberAlreadyRequested: status.HTTP_400_BAD_REQUEST,
            SubscriptionAccessLevelInvalid: status.HTTP_400_BAD_REQUEST,
            WebhookHasInvalidSignature: status.HTTP_403_FORBIDDEN,
            InvalidLabourUpdateRequest: status.HTTP_400_BAD_REQUEST,
        }
    )

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
