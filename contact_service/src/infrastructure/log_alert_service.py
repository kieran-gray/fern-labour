import logging

from src.application.alert_service import AlertService

log = logging.getLogger(__name__)


class LogAlertService(AlertService):
    async def send_alert(self, message: str) -> None:
        log.info(message)
