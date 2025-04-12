from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from app.api.dependencies import bearer_scheme
from app.api.exception_handler import ExceptionSchema
from app.labour.presentation.api.schemas.requests.subscription import (
    BlockSubscriberRequest,
    RemoveSubscriberRequest,
    UpdateContactMethodsRequest,
    UpdateRoleRequest,
)
from app.labour.presentation.api.schemas.responses.subscription import SubscriptionResponse
from app.setup.ioc.di_component_enum import ComponentEnum
from app.subscription.application.services.subscription_management_service import (
    SubscriptionManagementService,
)
from app.user.infrastructure.auth.interfaces.controller import AuthController

subscription_management_router = APIRouter(
    prefix="/subscription-management", tags=["Subscription Management"]
)


@subscription_management_router.put(
    "/remove-subscriber",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def remove_subscriber(
    request_data: RemoveSubscriberRequest,
    service: Annotated[SubscriptionManagementService, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscription = await service.remove_subscriber(
        requester_id=user.id, subscription_id=request_data.subscription_id
    )
    return SubscriptionResponse(subscription=subscription)


@subscription_management_router.put(
    "/block-subscriber",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def block_subscriber(
    request_data: BlockSubscriberRequest,
    service: Annotated[SubscriptionManagementService, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscription = await service.block_subscriber(
        requester_id=user.id, subscription_id=request_data.subscription_id
    )
    return SubscriptionResponse(subscription=subscription)


@subscription_management_router.put(
    "/update-role",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def update_role(
    request_data: UpdateRoleRequest,
    service: Annotated[SubscriptionManagementService, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscription = await service.update_role(
        requester_id=user.id, subscription_id=request_data.subscription_id, role=request_data.role
    )
    return SubscriptionResponse(subscription=subscription)


@subscription_management_router.put(
    "/update-contact-methods",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def update_contact_methods(
    request_data: UpdateContactMethodsRequest,
    service: Annotated[SubscriptionManagementService, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscription = await service.update_contact_methods(
        requester_id=user.id,
        subscription_id=request_data.subscription_id,
        contact_methods=request_data.contact_methods,
    )
    return SubscriptionResponse(subscription=subscription)
