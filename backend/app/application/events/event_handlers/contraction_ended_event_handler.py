import logging
from typing import Any

from app.application.events.event_handler import EventHandler
from app.application.notifications.entity import Notification
from app.application.notifications.notification_service import NotificationService
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.subscriber_service import SubscriberService
from app.domain.labour.exceptions import LabourNotFoundById
from app.domain.labour.repository import LabourRepository
from app.domain.labour.vo_labour_id import LabourId
from app.domain.services.should_go_to_hospital import ShouldGoToHospitalService
from app.domain.subscriber.enums import ContactMethod

log = logging.getLogger(__name__)


class ContractionEndedEventHandler(EventHandler):
    def __init__(
        self,
        labour_repository: LabourRepository,
        birthing_person_service: BirthingPersonService,
        subscriber_service: SubscriberService,
        notification_service: NotificationService,
    ):
        self._labour_repository = labour_repository
        self._birthing_person_service = birthing_person_service
        self._subscriber_service = subscriber_service
        self._notification_service = notification_service

    async def handle(self, event: dict[str, Any]) -> None:
        labour_id = event["data"]["labour_id"]
        labour = await self._labour_repository.get_by_id(LabourId(labour_id))
        if not labour:
            raise LabourNotFoundById(labour_id=labour_id)

        if not ShouldGoToHospitalService().should_go_to_hospital(labour):
            return

        birthing_person = await self._birthing_person_service.get_birthing_person(
            labour.birthing_person_id.value
        )

        # TODO refactor this event handler to trigger a notification event for each subscriber to
        # prevent failure when one subscriber in list is missing etc
        for subscriber_id in birthing_person.subscribers:
            subscriber = await self._subscriber_service.get(subscriber_id)
            message = (
                f"{subscriber.first_name}, it's time to take {birthing_person.first_name} "
                f"{birthing_person.last_name} to the hospital"
            )
            for method in subscriber.contact_methods:
                destination = subscriber.destination(method)
                if not destination:
                    continue
                notification = Notification(
                    type=ContactMethod(method), destination=destination, message=message
                )
                await self._notification_service.send(notification)
