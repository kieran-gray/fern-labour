from typing import Protocol

from app.infrastructure.auth.interfaces.models import User


class AuthService(Protocol):
    def authenticate_user(self, username: str, password: str) -> str:
        """
        Authenticate the user and return an access token.
        """

    def verify_token(self, token: str) -> User:
        """
        Verify the given token and return user information.
        """
