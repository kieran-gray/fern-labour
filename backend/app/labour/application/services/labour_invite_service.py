import logging

from app.labour.application.security.token_generator import TokenGenerator
from app.notification.application.dtos.notification import NotificationContent
from app.notification.application.dtos.notification_data import LabourInviteData
from app.notification.application.services.email_generation_service import EmailGenerationService
from app.notification.application.services.notification_service import NotificationService
from app.subscription.application.services.subscription_service import SubscriptionService
from app.subscription.domain.enums import ContactMethod
from app.subscription.domain.exceptions import SubscriberAlreadySubscribed
from app.user.application.dtos.user import UserDTO
from app.user.application.services.user_service import UserService

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
        self._template = "labour_invite.html"

    def _generate_notification_data(
        self, birthing_person: UserDTO, labour_id: str
    ) -> LabourInviteData:
        token = self._token_generator.generate(labour_id)
        return LabourInviteData(
            birthing_person_name=f"{birthing_person.first_name} {birthing_person.last_name}",
            birthing_person_first_name=birthing_person.first_name,
            link=f"https://track.fernlabour.com/subscribe/{labour_id}?token={token}",
        )

    def _generate_email(self, data: LabourInviteData) -> NotificationContent:
        subject = "Special invitation: Follow our baby's arrival journey 👶"
        message = self._email_generation_service.generate(self._template, data.to_dict())
        return NotificationContent(message=message, subject=subject)

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

        notification_data = self._generate_notification_data(
            birthing_person=birthing_person, labour_id=labour_id
        )
        notification_content = self._generate_email(data=notification_data)
        notification = await self._notification_service.create_notification(
            type=ContactMethod.EMAIL,
            destination=invite_email,
            template=self._template,
            data=notification_data.to_dict(),
            labour_id=labour_id,
            from_user_id=birthing_person_id,
        )
        notification.add_notification_content(content=notification_content)
        await self._notification_service.send(notification)
