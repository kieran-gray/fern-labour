from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_service import SubscriptionService
from app.infrastructure.auth.interfaces.controller import AuthController
from app.presentation.api.dependencies import bearer_scheme
from app.presentation.api.schemas.requests.subscriber import (
    RegisterSubscriberRequest,
    SubscribeToRequest,
    UnsubscribeFromRequest,
)
from app.presentation.api.schemas.responses.subscriber import (
    SubscriberListResponse,
    SubscriberResponse,
)
from app.presentation.api.schemas.responses.subscription import GetSubscriptionsResponse
from app.presentation.exception_handler import ExceptionSchema
from app.setup.ioc.di_component_enum import ComponentEnum

subscriber_router = APIRouter(prefix="/subscriber", tags=["Subscriber"])


@subscriber_router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": SubscriberResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get(
    service: Annotated[SubscriberService, FromComponent(ComponentEnum.SUBSCRIBER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriberResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriber = await service.get(subscriber_id=user.id)
    return SubscriberResponse(subscriber=subscriber)


@subscriber_router.post(
    "/register",
    responses={
        status.HTTP_200_OK: {"model": SubscriberResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def register(
    request_data: RegisterSubscriberRequest,
    service: Annotated[SubscriberService, FromComponent(ComponentEnum.SUBSCRIBER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriberResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriber = await service.register(
        subscriber_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        contact_methods=request_data.contact_methods,
        phone_number=user.phone_number,
        email=user.email,
    )
    return SubscriberResponse(subscriber=subscriber)


@subscriber_router.post(
    "/subscribe_to/{birthing_person_id}",
    responses={
        status.HTTP_200_OK: {"model": SubscriberResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def subscribe_to(
    birthing_person_id: str,
    request_data: SubscribeToRequest,
    service: Annotated[SubscriptionService, FromComponent(ComponentEnum.SUBSCRIBER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriberResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriber = await service.subscribe_to(
        subscriber_id=user.id, birthing_person_id=birthing_person_id, token=request_data.token
    )
    return SubscriberResponse(subscriber=subscriber)


@subscriber_router.post(
    "/unsubscribe_from",
    responses={
        status.HTTP_200_OK: {"model": SubscriberResponse},
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
) -> SubscriberResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriber = await service.unsubscribe_from(
        subscriber_id=user.id, birthing_person_id=request_data.birthing_person_id
    )
    return SubscriberResponse(subscriber=subscriber)


@subscriber_router.get(
    "/subscriptions",
    responses={
        status.HTTP_200_OK: {"model": GetSubscriptionsResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_subscriptions(
    subscriber_service: Annotated[SubscriberService, FromComponent(ComponentEnum.SUBSCRIBER)],
    birthing_person_service: Annotated[BirthingPersonService, FromComponent(ComponentEnum.LABOUR)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> GetSubscriptionsResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    subscriber = await subscriber_service.get(subscriber_id=user.id)
    birthing_person_summaries = [
        await birthing_person_service.get_birthing_person_summary(birthing_person_id)
        for birthing_person_id in subscriber.subscribed_to
    ]
    return GetSubscriptionsResponse(subscriptions=birthing_person_summaries)


@subscriber_router.get(
    "/subscribers",
    responses={
        status.HTTP_200_OK: {"model": SubscriberListResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_subscribers(
    birthing_person_service: Annotated[BirthingPersonService, FromComponent(ComponentEnum.LABOUR)],
    subscriber_service: Annotated[SubscriberService, FromComponent(ComponentEnum.SUBSCRIBER)],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> SubscriberListResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    birthing_person = await birthing_person_service.get_birthing_person(birthing_person_id=user.id)
    subscribers = await subscriber_service.get_many(birthing_person.subscribers)
    return SubscriberListResponse(subscribers=subscribers)
