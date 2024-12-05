from abc import abstractmethod
from typing import Protocol


class PasswordHasherInterface(Protocol):
    @abstractmethod
    def hash(self, raw_password: str) -> bytes: ...

    @abstractmethod
    def verify(self, *, raw_password: str, hashed_password: bytes) -> bool: ...
