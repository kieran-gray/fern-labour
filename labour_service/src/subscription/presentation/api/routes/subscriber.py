from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from src.api.dependencies import bearer_scheme
from src.api.exception_handler import ExceptionSchema
from src.setup.ioc.di_component_enum import ComponentEnum
from src.subscription.application.services.subscriber_invite_service import SubscriberInviteService
from src.subscription.presentation.api.schema.requests.subscriber import SendSubscriberInviteRequest
from src.user.infrastructure.auth.interfaces.controller import AuthController

subscriber_router = APIRouter(prefix="/subscriber", tags=["Subscriber"])


@subscriber_router.post(
    "/send_invite",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def send_invite(
    request_data: SendSubscriberInviteRequest,
    subscriber_invite_service: Annotated[
        SubscriberInviteService, FromComponent(ComponentEnum.INVITES)
    ],
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    await subscriber_invite_service.send_invite(
        subscriber_id=user.id,
        invite_email=request_data.invite_email,
    )
    return None
