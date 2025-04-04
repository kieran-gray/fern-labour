from typing import Protocol

from app.user.application.dtos.user import UserDTO


class AuthService(Protocol):
    def authenticate_user(self, username: str, password: str) -> str:
        """
        Authenticate the user and return an access token.
        """

    def verify_token(self, token: str) -> UserDTO:
        """
        Verify the given token and return user information.
        """
