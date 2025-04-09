import logging
from dataclasses import dataclass

from app.common.domain.producer import EventProducer
from app.labour.application.security.token_generator import TokenGenerator
from app.notification.application.dtos.notification_data import LabourInviteData
from app.notification.domain.enums import NotificationTemplate
from app.notification.domain.events import NotificationRequested
from app.subscription.application.services.subscription_query_service import (
    SubscriptionQueryService,
)
from app.subscription.domain.enums import ContactMethod
from app.subscription.domain.exceptions import SubscriberAlreadySubscribed
from app.user.application.dtos.user import UserDTO
from app.user.application.services.user_service import UserService

log = logging.getLogger(__name__)


@dataclass
class LabourInviteNotificationMetadata:
    labour_id: str
    from_user_id: str

    def to_dict(self) -> dict[str, str]:
        return {
            "labour_id": self.labour_id,
            "from_user_id": self.from_user_id,
        }


class LabourInviteService:
    def __init__(
        self,
        user_service: UserService,
        event_producer: EventProducer,
        subscription_query_service: SubscriptionQueryService,
        token_generator: TokenGenerator,
    ):
        self._user_service = user_service
        self._event_producer = event_producer
        self._subscription_query_service = subscription_query_service
        self._token_generator = token_generator
        self._template = NotificationTemplate.LABOUR_INVITE

    def _generate_notification_data(
        self, birthing_person: UserDTO, labour_id: str
    ) -> LabourInviteData:
        token = self._token_generator.generate(labour_id)
        return LabourInviteData(
            birthing_person_name=f"{birthing_person.first_name} {birthing_person.last_name}",
            birthing_person_first_name=birthing_person.first_name,
            link=f"https://track.fernlabour.com/subscribe/{labour_id}?token={token}",
        )

    async def send_invite(self, birthing_person_id: str, labour_id: str, invite_email: str) -> None:
        birthing_person = await self._user_service.get(birthing_person_id)
        subscriptions = await self._subscription_query_service.get_labour_subscriptions(
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
        notification_metadata = LabourInviteNotificationMetadata(
            labour_id=labour_id,
            from_user_id=birthing_person_id,
        )
        notification_event = NotificationRequested.create(
            data={
                "type": ContactMethod.EMAIL,
                "destination": invite_email,
                "template": self._template.value,
                "data": notification_data.to_dict(),
                "metadata": notification_metadata.to_dict(),
            }
        )
        await self._event_producer.publish(event=notification_event)
