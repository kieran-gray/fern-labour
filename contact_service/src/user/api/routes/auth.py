from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Form

from src.user.infrastructure.auth.interfaces.controller import AuthController
from src.user.infrastructure.auth.interfaces.schemas import TokenResponse

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
