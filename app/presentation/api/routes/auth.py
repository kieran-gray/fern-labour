from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from app.application.base.enums import ResponseStatusEnum
from app.application.dtos.requests.auth import LogInRequest, SignUpRequest
from app.application.dtos.responses.auth import LogInResponse, LogOutResponse, SignUpResponse
from app.application.services.account_service import AccountService
from app.presentation.exception_handler import ExceptionSchema

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"model": LogInResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def log_in(
    request_data: LogInRequest,
    service: FromDishka[AccountService],
) -> LogInResponse:
    """Log in."""
    await service.log_in(request_data.username, request_data.password)
    return LogInResponse(message="Successfully logged out.")


@auth_router.post(
    "/logout",
    responses={
        status.HTTP_200_OK: {"model": LogOutResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def log_out(
    service: FromDishka[AccountService],
) -> LogOutResponse:
    """Log out."""
    await service.log_out()
    return LogOutResponse(message="Successfully logged out.")


@auth_router.post(
    "/sign-up",
    responses={
        status.HTTP_200_OK: {"model": SignUpResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def sign_up(
    request_data: SignUpRequest,
    service: FromDishka[AccountService],
) -> SignUpResponse:
    """Sign up."""
    await service.sign_up(request_data.username, request_data.password)
    return SignUpResponse(username=request_data.username, status=ResponseStatusEnum.CREATED)
