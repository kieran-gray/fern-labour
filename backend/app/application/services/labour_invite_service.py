import logging

from app.application.dtos.user import UserDTO
from app.application.notifications.email_generation_service import EmailGenerationService
from app.application.notifications.entity import Notification
from app.application.notifications.notification_service import NotificationService
from app.application.security.token_generator import TokenGenerator
from app.application.services.subscription_service import SubscriptionService
from app.application.services.user_service import UserService
from app.domain.subscription.enums import ContactMethod
from app.domain.subscription.exceptions import SubscriberAlreadySubscribed

log = logging.getLogger(__name__)


class LabourInviteService:
    def __init__(
        self,
        user_service: UserService,
        notification_service: NotificationService,
        subscription_service: SubscriptionService,
        email_generation_service: EmailGenerationService,
        token_generator: TokenGenerator,
    ):
        self._user_service = user_service
        self._notification_service = notification_service
        self._subscription_service = subscription_service
        self._email_generation_service = email_generation_service
        self._token_generator = token_generator

    def _generate_email(
        self,
        birthing_person: UserDTO,
        labour_id: str,
        destination: str,
    ) -> Notification:
        subject = "Special invitation: Follow our baby's arrival journey 👶"
        token = self._token_generator.generate(labour_id)

        email_data = {
            "birthing_person_name": f"{birthing_person.first_name} {birthing_person.last_name}",
            "birthing_person_first_name": birthing_person.first_name,
            "link": f"https://track.fernlabour.com/subscribe/{labour_id}?token={token}",
        }
        message = self._email_generation_service.generate("labour_invite.html", email_data)
        return Notification(
            type=ContactMethod.EMAIL, destination=destination, message=message, subject=subject
        )

    async def send_invite(self, birthing_person_id: str, labour_id: str, invite_email: str) -> None:
        birthing_person = await self._user_service.get(birthing_person_id)
        subscriptions = await self._subscription_service.get_labour_subscriptions(
            requester_id=birthing_person_id, labour_id=labour_id
        )
        subscriber_ids = [subscription.subscriber_id for subscription in subscriptions]

        subscribers = await self._user_service.get_many(subscriber_ids)
        subscriber_emails = [subscriber.email for subscriber in subscribers]
        if invite_email in subscriber_emails:
            raise SubscriberAlreadySubscribed()

        notification = self._generate_email(
            birthing_person=birthing_person, labour_id=labour_id, destination=invite_email
        )
        await self._notification_service.send(notification)
