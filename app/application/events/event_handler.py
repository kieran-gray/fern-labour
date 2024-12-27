from abc import ABC, abstractmethod
from typing import Any


class EventHandler(ABC):
    topic: str

    @abstractmethod
    async def handle(self, event: dict[str, Any]) -> None:
        pass
