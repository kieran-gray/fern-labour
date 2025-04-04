from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from app.application.services.subscription_service import SubscriptionService
from app.application.services.user_service import UserService
from app.infrastructure.auth.interfaces.controller import AuthController
from app.labour.application.services.get_labour_service import GetLabourService
from app.presentation.api.dependencies import bearer_scheme
from app.presentation.api.schemas.requests.subscription import (
    SubscribeToRequest,
    UnsubscribeFromRequest,
)
from app.presentation.api.schemas.responses.subscription import (
    LabourSubscriptionsResponse,
    SubscriberSubscriptionsResponse,
    SubscriptionDataResponse,
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
    service: Annotated[SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
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
    service: Annotated[SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
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
    service: Annotated[SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionsResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriptions = await service.get_subscriber_subscriptions(subscriber_id=user.id)
    return SubscriptionsResponse(subscriptions=subscriptions)


@subscription_router.get(
    "/subscriber_subscriptions",
    responses={
        status.HTTP_200_OK: {"model": SubscriberSubscriptionsResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_subscriber_subscriptions(
    subscription_service: Annotated[
        SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
    ],
    user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriberSubscriptionsResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriptions = await subscription_service.get_subscriber_subscriptions(subscriber_id=user.id)
    birthing_persons = await user_service.get_many_summary(
        user_ids=[subscription.birthing_person_id for subscription in subscriptions]
    )
    return SubscriberSubscriptionsResponse(
        subscriptions=subscriptions, birthing_persons=birthing_persons
    )


@subscription_router.get(
    "/subscription-data/{subscription_id}",
    responses={
        status.HTTP_200_OK: {"model": SubscriptionDataResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_subscription_by_id(
    subscription_id: str,
    subscription_service: Annotated[
        SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
    ],
    user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
    get_labour_service: Annotated[GetLabourService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriptionDataResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscription = await subscription_service.get_by_id(
        requester_id=user.id, subscription_id=subscription_id
    )
    birthing_person = await user_service.get_summary(user_id=subscription.birthing_person_id)
    labour = await get_labour_service.get_labour_by_id(labour_id=subscription.labour_id)
    return SubscriptionDataResponse(
        subscription=subscription, birthing_person=birthing_person, labour=labour
    )


@subscription_router.get(
    "/labour_subscriptions/{labour_id}",
    responses={
        status.HTTP_200_OK: {"model": LabourSubscriptionsResponse},
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
    subscription_service: Annotated[
        SubscriptionService, FromComponent(ComponentEnum.SUBSCRIPTIONS)
    ],
    user_service: Annotated[UserService, FromComponent(ComponentEnum.USER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> LabourSubscriptionsResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriptions = await subscription_service.get_labour_subscriptions(
        requester_id=user.id, labour_id=labour_id
    )
    subscribers = await user_service.get_many_summary(
        user_ids=[subscription.subscriber_id for subscription in subscriptions]
    )
    return LabourSubscriptionsResponse(subscriptions=subscriptions, subscribers=subscribers)
