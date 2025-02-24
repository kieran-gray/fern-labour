from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Form
from fastapi.security import HTTPAuthorizationCredentials

from app.application.dtos.user import UserDTO
from app.infrastructure.auth.interfaces.controller import AuthController
from app.infrastructure.auth.interfaces.schemas import TokenResponse
from app.presentation.api.dependencies import bearer_scheme

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# Define the login endpoint
@auth_router.post("/login", response_model=TokenResponse)
@inject
async def login(
    auth_controller: Annotated[AuthController, FromComponent()],
    username: str = Form(...),
    password: str = Form(...),
) -> TokenResponse:
    """
    Login endpoint to authenticate the user and return an access token.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user.

    Returns:
        TokenResponse: Contains the access token upon successful authentication.
    """
    return auth_controller.login(username, password)


# Define the protected endpoint
@auth_router.get("/user", response_model=UserDTO)
@inject
async def get_user(
    auth_controller: Annotated[AuthController, FromComponent()],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UserDTO:
    """
    Get currently logged in user. Requires a valid token for access.

    Args:
        credentials (HTTPAuthorizationCredentials):
            Bearer token provided via HTTP Authorization header.

    Returns:
        User: Information about the authenticated user.
    """
    return auth_controller.get_authenticated_user(credentials)
