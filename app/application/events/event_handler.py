from typing import Any, Protocol


class EventHandler(Protocol):
    async def handle(self, event: dict[str, Any]) -> None: ...
