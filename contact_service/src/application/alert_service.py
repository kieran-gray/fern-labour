import logging
from typing import Protocol, runtime_checkable

log = logging.getLogger(__name__)


@runtime_checkable
class AlertService(Protocol):
    async def send_alert(self, message: str) -> None: ...
