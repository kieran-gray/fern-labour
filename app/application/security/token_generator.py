from typing import Protocol


class TokenGenerator(Protocol):
    """Protocol for a token operations."""

    def generate(self, input: str) -> str: ...

    def validate(self, id: str, token: str) -> bool: ...
