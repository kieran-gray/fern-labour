import logging
from typing import Any, Protocol

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.application.dtos.subscriber import SubscriberDTO
from app.application.events.event_handler import EventHandler
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.entity import Notification
from app.application.notifications.notification_service import NotificationService
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.subscriber_service import SubscriberService
from app.application.services.subscription_service import SubscriptionService
from app.domain.subscriber.exceptions import SubscriberNotFoundById
from app.domain.subscription.enums import ContactMethod

log = logging.getLogger(__name__)


class LabourCompletedNotificationGenerator(Protocol):
    def __call__(
        self,
        birthing_person: BirthingPersonDTO,
        subscriber: SubscriberDTO,
        notes: str,
        destination: str,
    ) -> Notification: ...


class LabourCompletedEventHandler(EventHandler):
    def __init__(
        self,
        birthing_person_service: BirthingPersonService,
        subscriber_service: SubscriberService,
        subscription_service: SubscriptionService,
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
    ):
        self._birthing_person_service = birthing_person_service
        self._subscriber_service = subscriber_service
        self._subscription_service = subscription_service
        self._notification_service = notification_service
        self._email_generation_service = email_generation_service

    def _generate_email(
        self,
        birthing_person: BirthingPersonDTO,
        subscriber: SubscriberDTO,
        notes: str,
        destination: str,
    ) -> Notification:
        subject = f"Labour update from {birthing_person.first_name} {birthing_person.last_name}"
        update = f"{birthing_person.first_name} has completed labour!"
        if notes:
            update += f"\n\nThey added the following note:\n\n{notes}"

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
        notes: str,
        destination: str,
    ) -> Notification:
        message = (
            f"Hey {subscriber.first_name}, {birthing_person.first_name} {birthing_person.last_name}"
            " has completed labour!"
        )
        if notes:
            message += f"\nThey added the following note:\n{notes}"

        return Notification(
            type=ContactMethod.SMS,
            destination=destination,
            message=message,
        )

    def _get_notification_generator(
        self, contact_method: str
    ) -> LabourCompletedNotificationGenerator:
        # TODO this could be refactored into a notification generation service
        contact_method = ContactMethod(contact_method)
        if contact_method is ContactMethod.EMAIL:
            return self._generate_email
        elif contact_method is ContactMethod.SMS:
            return self._generate_sms
        raise NotImplementedError(f"Notification generator for {contact_method} not implemented")

    async def handle(self, event: dict[str, Any]) -> None:
        birthing_person_id = event["data"]["birthing_person_id"]
        labour_id = event["data"]["labour_id"]

        birthing_person = await self._birthing_person_service.get(
            birthing_person_id=birthing_person_id
        )
        subscriptions = await self._subscription_service.get_labour_subscriptions(
            requester_id=birthing_person_id, labour_id=labour_id
        )

        for subscription in subscriptions:
            try:
                subscriber = await self._subscriber_service.get(subscription.subscriber_id)
            except SubscriberNotFoundById as err:
                log.error(err)
                continue

            for method in subscription.contact_methods:
                if destination := subscriber.destination(method):
                    notification = self._get_notification_generator(method)(
                        birthing_person=birthing_person,
                        subscriber=subscriber,
                        notes=event["data"]["notes"],
                        destination=destination,
                    )
                    await self._notification_service.send(notification)
