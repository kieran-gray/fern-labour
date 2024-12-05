from abc import abstractmethod
from typing import Protocol


class CommitterInterface(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        """
        :raises GatewayError:
        """
