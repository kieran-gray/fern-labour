from abc import ABC, abstractmethod
from typing import Any


class NotificationGateway(ABC):
    """Repository interface for LaborSession aggregate root"""

    @abstractmethod
    async def send(self, data: dict[str, Any]) -> None:
        """
        Send a notification.

        Args:
            data: The data to send
        """
