from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GrantAdminRequest:
    username: str
