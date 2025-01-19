import logging
from typing import Any

from app.application.dtos.birthing_person import BirthingPersonDTO
from app.application.events.event_handler import EventHandler
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.entity import Notification
from app.application.notifications.notification_service import NotificationService
from app.application.security.token_generator import TokenGenerator
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.subscriber_service import SubscriberService
from app.domain.subscriber.enums import ContactMethod
from app.domain.subscriber.exceptions import SubscriberAlreadySubscribedToBirthingPerson

log = logging.getLogger(__name__)


class BirthingPersonSendInviteEventHandler(EventHandler):
    def __init__(
        self,
        birthing_person_service: BirthingPersonService,
        notification_service: NotificationService,
        subscriber_service: SubscriberService,
        email_generation_service: EmailGenerationService,
        token_generator: TokenGenerator,
    ):
        self._birthing_person_service = birthing_person_service
        self._notification_service = notification_service
        self._subscriber_service = subscriber_service
        self._email_generation_service = email_generation_service
        self._token_generator = token_generator

    def _generate_email(
        self,
        birthing_person: BirthingPersonDTO,
        destination: str,
    ) -> Notification:
        subject = "Special invitation: Follow our baby's arrival journey 👶"
        token = self._token_generator.generate(birthing_person.id)

        email_data = {
            "birthing_person_name": f"{birthing_person.first_name} {birthing_person.last_name}",
            "birthing_person_first_name": birthing_person.first_name,
            "link": f"https://fernlabour.com/subscribe/{birthing_person.id}?token={token}",
        }
        message = self._email_generation_service.generate("labour_invite.html", email_data)
        return Notification(
            type=ContactMethod.EMAIL, destination=destination, message=message, subject=subject
        )

    async def handle(self, event: dict[str, Any]) -> None:
        birthing_person_id = event["data"]["birthing_person_id"]
        birthing_person = await self._birthing_person_service.get_birthing_person(
            birthing_person_id
        )
        destination = event["data"]["invite_email"]
        subscribers = await self._subscriber_service.get_many(birthing_person.subscribers)
        subscriber_emails = [subscriber.email for subscriber in subscribers]
        if destination in subscriber_emails:
            raise SubscriberAlreadySubscribedToBirthingPerson()

        notification = self._generate_email(birthing_person, destination)
        await self._notification_service.send(notification)
