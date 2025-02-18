import logging

from app.application.dtos.subscriber import SubscriberDTO
from app.application.security.token_generator import TokenGenerator
from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.exceptions import SubscriberExistsWithID, SubscriberNotFoundById
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscriber.vo_subscriber_id import SubscriberId

log = logging.getLogger(__name__)


class SubscriberService:
    def __init__(
        self,
        subscriber_repository: SubscriberRepository,
        token_generator: TokenGenerator,
    ):
        self._subscriber_repository = subscriber_repository
        self._token_generator = token_generator

    async def register(
        self,
        subscriber_id: str,
        first_name: str,
        last_name: str,
        phone_number: str | None = None,
        email: str | None = None,
    ) -> SubscriberDTO:
        domain_id = SubscriberId(subscriber_id)
        subscriber = await self._subscriber_repository.get_by_id(domain_id)
        if subscriber:
            raise SubscriberExistsWithID(subscriber_id=subscriber_id)

        subscriber = Subscriber.create(
            id=subscriber_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
        )
        await self._subscriber_repository.save(subscriber)
        return SubscriberDTO.from_domain(subscriber)

    async def get(self, subscriber_id: str) -> SubscriberDTO:
        domain_id = SubscriberId(subscriber_id)
        subscriber = await self._subscriber_repository.get_by_id(domain_id)
        if not subscriber:
            raise SubscriberNotFoundById(subscriber_id=subscriber_id)
        return SubscriberDTO.from_domain(subscriber)

    async def get_many(self, subscriber_ids: list[str]) -> list[SubscriberDTO]:
        domain_ids = [SubscriberId(subscriber_id) for subscriber_id in subscriber_ids]
        subscribers = await self._subscriber_repository.get_by_ids(domain_ids)
        return [SubscriberDTO.from_domain(subscriber) for subscriber in subscribers]
