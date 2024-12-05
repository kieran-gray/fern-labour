from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReactivateUserRequest:
    username: str
