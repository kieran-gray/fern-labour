from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.infrastructure.auth.interfaces.models import User
from app.infrastructure.auth.interfaces.schemas import TokenResponse
from app.infrastructure.auth.interfaces.service import AuthService

# Initialize HTTPBearer security dependency
bearer_scheme = HTTPBearer()


class KeycloakAuthController:
    """
    Controller for handling authentication logic.
    """

    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    def login(self, username: str = Form(...), password: str = Form(...)) -> TokenResponse:
        """
        Authenticate user and return access token.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password of the user.

        Raises:
            HTTPException: If the authentication fails (wrong credentials).

        Returns:
            TokenResponse: Contains the access token upon successful authentication.
        """
        access_token = self._auth_service.authenticate_user(username, password)

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return TokenResponse(access_token=access_token)

    def get_authenticated_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ) -> User:
        """
        Access a protected resource that requires valid token authentication.

        Args:
            credentials (HTTPAuthorizationCredentials): Bearer token provided via HTTP Authorization header.

        Raises:
            HTTPException: If the token is invalid or not provided.

        Returns:
            User: Information about the authenticated user.
        """
        token = credentials.credentials

        user_info = self._auth_service.verify_token(token)

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_info
