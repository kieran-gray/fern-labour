from abc import ABC, abstractmethod


class TokenGenerator(ABC):
    """Abstract base class for a token operations."""

    @abstractmethod
    def generate(self, input: str) -> str: ...

    @abstractmethod
    def validate(self, id: str, token: str) -> bool: ...
