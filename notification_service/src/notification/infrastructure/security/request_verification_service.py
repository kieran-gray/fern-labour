from typing import Any, Protocol


class RequestVerificationService(Protocol):
    def verify(self, uri: Any, params: Any, signature: Any) -> None: ...
