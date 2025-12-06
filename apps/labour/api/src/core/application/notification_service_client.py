import logging
import httpx

from fern_labour_notifications_shared.event_data import NotificationRequestedData

log = logging.getLogger(__name__)


class NotificationServiceClient:
    def __init__(self, notification_service_url: str) -> None:
        self._notification_service_url = notification_service_url

    async def request_notification(self, request: NotificationRequestedData) -> None:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._notification_service_url,
                    json=request.to_dict(),
                    timeout=10.0,
                )
                response.raise_for_status()
            except httpx.ConnectError as err:
                log.error(
                    f"Connection error sending notification: {err}. "
                    f"Is the notification service running at {self._notification_service_url}?"
                )
            except httpx.HTTPError as err:
                log.error(
                    f"Failed to send notification: {err}"
                )
