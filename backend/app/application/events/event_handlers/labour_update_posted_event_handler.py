import logging
from typing import Any, Protocol

from app.application.dtos.notification import NotificationContent
from app.application.dtos.user import UserDTO
from app.application.events.event_handler import EventHandler
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.notification_data import LabourUpdateData
from app.application.notifications.notification_service import NotificationService
from app.application.services.subscription_service import SubscriptionService
from app.application.services.user_service import UserService
from app.domain.base.event import DomainEvent
from app.domain.labour_update.enums import LabourUpdateType
from app.domain.subscription.enums import ContactMethod
from app.domain.user.exceptions import UserNotFoundById

log = logging.getLogger(__name__)


class AnnouncementMadeNotificationGenerator(Protocol):
    def __call__(self, data: LabourUpdateData) -> NotificationContent: ...


class LabourUpdatePostedEventHandler(EventHandler):
    def __init__(
        self,
        user_service: UserService,
        subscription_service: SubscriptionService,
        notification_service: NotificationService,
        email_generation_service: EmailGenerationService,
        tracking_link: str,
    ):
        self._user_service = user_service
        self._subscription_service = subscription_service
        self._notification_service = notification_service
        self._email_generation_service = email_generation_service
        self._tracking_link = tracking_link
        self._template = "labour_update.html"

    def _generate_notification_data(
        self,
        birthing_person: UserDTO,
        subscriber: UserDTO,
        announcement: str,
    ) -> LabourUpdateData:
        return LabourUpdateData(
            birthing_person_name=f"{birthing_person.first_name} {birthing_person.last_name}",
            subscriber_first_name=subscriber.first_name,
            update=f"{birthing_person.first_name} has just made an announcement:\n\n{announcement}",
            notes=announcement,
            link=self._tracking_link,
        )

    def _generate_email(self, data: LabourUpdateData) -> NotificationContent:
        subject = f"Labour update from {data.birthing_person_name}"
        message = self._email_generation_service.generate(self._template, data.to_dict())
        return NotificationContent(message=message, subject=subject)

    def _generate_sms(self, data: LabourUpdateData) -> NotificationContent:
        message = (
            f"Hey {data.subscriber_first_name}, {data.birthing_person_name}"
            f" has just made an announcement:\n{data.notes}"
        )
        return NotificationContent(message=message)

    def _get_notification_content_generator(
        self, contact_method: str
    ) -> AnnouncementMadeNotificationGenerator:
        contact_method = ContactMethod(contact_method)
        if contact_method is ContactMethod.EMAIL:
            return self._generate_email
        elif contact_method is ContactMethod.SMS:
            return self._generate_sms
        raise NotImplementedError(f"Notification generator for {contact_method} not implemented")

    async def handle(self, event: dict[str, Any]) -> None:
        domain_event = DomainEvent.from_dict(event=event)
        if domain_event.data["labour_update_type"] == LabourUpdateType.STATUS_UPDATE.value:
            return

        birthing_person_id = domain_event.data["birthing_person_id"]
        labour_id = domain_event.data["labour_id"]
        labour_update_id = domain_event.data["labour_update_id"]

        birthing_person = await self._user_service.get(user_id=birthing_person_id)

        subscriptions = await self._subscription_service.get_labour_subscriptions(
            requester_id=birthing_person_id, labour_id=labour_id
        )

        for subscription in subscriptions:
            try:
                subscriber = await self._user_service.get(user_id=subscription.subscriber_id)
            except UserNotFoundById as err:
                log.error(err)
                continue

            for method in subscription.contact_methods:
                destination = subscriber.destination(method)
                if not destination:
                    continue

                notification_data = self._generate_notification_data(
                    birthing_person=birthing_person,
                    subscriber=subscriber,
                    announcement=domain_event.data["message"],
                )
                notification_generator = self._get_notification_content_generator(method)
                notification_content = notification_generator(data=notification_data)
                notification = await self._notification_service.create_notification(
                    type=ContactMethod(method),
                    destination=destination,
                    template=self._template,
                    data=notification_data.to_dict(),
                    labour_id=labour_id,
                    birthing_person_id=birthing_person_id,
                    subscriber_id=subscriber.id,
                    labour_update_id=labour_update_id,
                )
                notification.add_notification_content(content=notification_content)
                await self._notification_service.send(notification)
