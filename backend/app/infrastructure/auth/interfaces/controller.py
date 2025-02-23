from typing import Protocol

from app.infrastructure.auth.interfaces.models import AuthorizationCredentials, User
from app.infrastructure.auth.interfaces.schemas import TokenResponse


class AuthController(Protocol):
    """
    Controller for handling authentication logic.
    """

    def login(self, username: str, password: str) -> TokenResponse:
        """
        Authenticate user and return access token.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password of the user.

        Raises:
            AuthorizationError: If the authentication fails (wrong credentials).

        Returns:
            TokenResponse: Contains the access token upon successful authentication.
        """

    def get_authenticated_user(self, credentials: AuthorizationCredentials) -> User:
        """
        Get currently authenticated user information. Requires valid token.

        Args:
            credentials (AuthorizationCredentials):
                Bearer token provided via HTTP Authorization header.

        Raises:
            AuthorizationError: If the token is invalid or not provided.

        Returns:
            User: Information about the authenticated user.
        """
