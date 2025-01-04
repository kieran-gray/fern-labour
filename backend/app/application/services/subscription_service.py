import logging

from app.application.dtos.subscriber import SubscriberDTO
from app.application.events.producer import EventProducer
from app.application.security.token_generator import TokenGenerator
from app.domain.birthing_person.exceptions import BirthingPersonNotFoundById
from app.domain.birthing_person.repository import BirthingPersonRepository
from app.domain.birthing_person.vo_birthing_person_id import BirthingPersonId
from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.exceptions import SubscriberNotFoundById, SubscriptionTokenIncorrect
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscriber.vo_subscriber_id import SubscriberId

log = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(
        self,
        birthing_person_repository: BirthingPersonRepository,
        subscriber_repository: SubscriberRepository,
        token_generator: TokenGenerator,
        event_producer: EventProducer,
    ):
        self._birthing_person_repository = birthing_person_repository
        self._subscriber_repository = subscriber_repository
        self._token_generator = token_generator
        self._event_producer = event_producer

    async def _get_subscriber(self, subscriber_id: str) -> Subscriber:
        domain_id = SubscriberId(subscriber_id)
        subscriber = await self._subscriber_repository.get_by_id(domain_id)
        if not subscriber:
            raise SubscriberNotFoundById(subscriber_id=subscriber_id)
        return subscriber

    async def subscribe_to(
        self, subscriber_id: str, birthing_person_id: str, token: str
    ) -> SubscriberDTO:
        subscriber = await self._get_subscriber(subscriber_id=subscriber_id)
        birthing_person_domain_id = BirthingPersonId(birthing_person_id)
        birthing_person = await self._birthing_person_repository.get_by_id(
            birthing_person_domain_id
        )
        if not birthing_person:
            raise BirthingPersonNotFoundById(birthing_person_id=birthing_person_id)

        if not self._token_generator.validate(birthing_person_id, token):
            raise SubscriptionTokenIncorrect()

        subscriber.subscribe_to(birthing_person_domain_id)
        await self._subscriber_repository.save(subscriber)

        await self._event_producer.publish_batch(subscriber.clear_domain_events())

        return SubscriberDTO.from_domain(subscriber)

    async def unsubscribe_from(self, subscriber_id: str, birthing_person_id: str) -> SubscriberDTO:
        subscriber = await self._get_subscriber(subscriber_id=subscriber_id)

        subscriber.unsubscribe_from(BirthingPersonId(birthing_person_id))
        await self._subscriber_repository.save(subscriber)

        await self._event_producer.publish_batch(subscriber.clear_domain_events())

        return SubscriberDTO.from_domain(subscriber)
