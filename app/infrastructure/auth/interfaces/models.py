from dataclasses import dataclass
from typing import Protocol


@dataclass
class User:
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str | None = None


class AuthorizationCredentials(Protocol):
    scheme: str
    credentials: str
