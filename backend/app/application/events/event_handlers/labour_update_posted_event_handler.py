import logging
from typing import Any, Protocol

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.domain.labour_update.enums import LabourUpdateType
from app.application.dtos.subscriber import SubscriberDTO
from app.application.events.event_handler import EventHandler
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.entity import Notification
from app.application.notifications.notification_service import NotificationService
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.subscriber_service import SubscriberService
from app.domain.subscriber.enums import ContactMethod
from app.domain.subscriber.exceptions import SubscriberNotFoundById

log = logging.getLogger(__name__)


class AnnouncementMadeNotificationGenerator(Protocol):
    def __call__(
        self,
        birthing_person: BirthingPersonDTO,
        subscriber: SubscriberDTO,
        announcement: str,
        destination: str,
    ) -> Notification: ...


class LabourUpdatePostedEventHandler(EventHandler):
    def __init__(
        self,
        birthing_person_service: BirthingPersonService,
        subscriber_service: SubscriberService,
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
    ):
        self._birthing_person_service = birthing_person_service
        self._subscriber_service = subscriber_service
        self._notification_service = notification_service
        self._email_generation_service = email_generation_service

    def _generate_email(
        self,
        birthing_person: BirthingPersonDTO,
        subscriber: SubscriberDTO,
        announcement: str,
        destination: str,
    ) -> Notification:
        subject = f"Labour update from {birthing_person.first_name} {birthing_person.last_name}"
        update = f"{birthing_person.first_name} has just made an announcement:\n\n{announcement}"

        email_data = {
            "birthing_person_name": f"{birthing_person.first_name} {birthing_person.last_name}",
            "subscriber_first_name": subscriber.first_name,
            "update": update,
            "link": "https://track.fernlabour.com",  # TODO not hardcoded
        }
        message = self._email_generation_service.generate("labour_update.html", email_data)
        return Notification(
            type=ContactMethod.EMAIL, destination=destination, message=message, subject=subject
        )

    def _generate_sms(
        self,
        birthing_person: BirthingPersonDTO,
        subscriber: SubscriberDTO,
        announcement: str,
        destination: str,
    ) -> Notification:
        message = (
            f"Hey {subscriber.first_name}, {birthing_person.first_name} {birthing_person.last_name}"
            f" has just made an announcement:\n{announcement}"
        )
        return Notification(
            type=ContactMethod.SMS,
            destination=destination,
            message=message,
        )

    def _get_notification_generator(
        self, contact_method: str
    ) -> AnnouncementMadeNotificationGenerator:
        contact_method = ContactMethod(contact_method)
        if contact_method is ContactMethod.EMAIL:
            return self._generate_email
        elif contact_method is ContactMethod.SMS:
            return self._generate_sms
        raise NotImplementedError(f"Notification generator for {contact_method} not implemented")

    async def handle(self, event: dict[str, Any]) -> None:
        if event["data"]["labour_update_type"] == LabourUpdateType.STATUS_UPDATE.value:
            return

        birthing_person_id = event["data"]["birthing_person_id"]
        birthing_person = await self._birthing_person_service.get_birthing_person(
            birthing_person_id
        )

        for subscriber_id in birthing_person.subscribers:
            try:
                subscriber = await self._subscriber_service.get(subscriber_id)
            except SubscriberNotFoundById as err:
                log.error(err)
                continue

            for method in subscriber.contact_methods:
                if destination := subscriber.destination(method):
                    notification = self._get_notification_generator(method)(
                        birthing_person=birthing_person,
                        subscriber=subscriber,
                        announcement=event["data"]["message"],
                        destination=destination,
                    )
                    await self._notification_service.send(notification)
