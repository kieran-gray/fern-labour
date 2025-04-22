from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from src.api.dependencies import bearer_scheme
from src.api.exception_handler import ExceptionSchema
from src.setup.ioc.di_component_enum import ComponentEnum
from src.user.infrastructure.auth.interfaces.controller import AuthController
from src.user.presentation.api.schemas.responses.user import UserResponse, UserSummaryResponse

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": UserResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_user(
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UserResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    return UserResponse(user=user)


@user_router.get(
    "/summary",
    responses={
        status.HTTP_200_OK: {"model": UserSummaryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_user_summary(
    auth_controller: Annotated[AuthController, FromComponent(ComponentEnum.DEFAULT)],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UserSummaryResponse:
    user = auth_controller.get_authenticated_user(credentials=credentials)
    return UserSummaryResponse(user=user.to_summary())
