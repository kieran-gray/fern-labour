from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from app.application.services.subscription_service import SubscriptionService
from app.infrastructure.auth.interfaces.controller import AuthController
from app.presentation.api.dependencies import bearer_scheme
from app.presentation.api.schemas.requests.subscriber import (
    SubscribeToRequest,
    UnsubscribeFromRequest,
)
from app.presentation.api.schemas.responses.subscription import (
    SubscriptionResponse,
    SubscriptionsResponse,
)
from app.presentation.exception_handler import ExceptionSchema
from app.setup.ioc.di_component_enum import ComponentEnum

subscription_router = APIRouter(prefix="/subscription", tags=["Subscription"])


@subscription_router.post(
    "/subscribe/{labour_id}",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def subscribe_to(
    labour_id: str,
    request_data: SubscribeToRequest,
    service: Annotated[SubscriptionService, FromComponent(ComponentEnum.SUBSCRIBER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscription = await service.subscribe_to(
        subscriber_id=user.id, labour_id=labour_id, token=request_data.token
    )
    return SubscriptionResponse(subscription=subscription)


@subscription_router.post(
    "/unsubscribe",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def unsubscribe_from(
    request_data: UnsubscribeFromRequest,
    service: Annotated[SubscriptionService, FromComponent(ComponentEnum.SUBSCRIBER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscription = await service.unsubscribe_from(
        subscriber_id=user.id, labour_id=request_data.labour_id
    )
    return SubscriptionResponse(subscription=subscription)


@subscription_router.get(
    "/subscriptions",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionsResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_subscriptions(
    service: Annotated[SubscriptionService, FromComponent(ComponentEnum.SUBSCRIBER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionsResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriptions = await service.get_subscriber_subscriptions(subscriber_id=user.id)
    return SubscriptionsResponse(subscriptions=subscriptions)


@subscription_router.get(
    "/labour_subscriptions/{labour_id}",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionsResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_labour_subscriptions(
    labour_id: str,
    subscription_service: Annotated[SubscriptionService, FromComponent(ComponentEnum.SUBSCRIBER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionsResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriptions = await subscription_service.get_labour_subscriptions(
        requester_id=user.id, labour_id=labour_id
    )
    return SubscriptionsResponse(subscriptions=subscriptions)
