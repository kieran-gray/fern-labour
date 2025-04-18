from typing import Protocol


class AuthorizationCredentials(Protocol):
    scheme: str
    credentials: str
