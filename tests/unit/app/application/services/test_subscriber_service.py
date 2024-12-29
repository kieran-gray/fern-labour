import pytest
import pytest_asyncio

from app.application.dtos.subscriber import SubscriberDTO
from app.application.security.token_generator import TokenGenerator
from app.application.services.subscriber_service import SubscriberService
from app.domain.subscriber.entity import Subscriber
from app.domain.subscriber.exceptions import SubscriberExistsWithID, SubscriberNotFoundById
from app.domain.subscriber.repository import SubscriberRepository
from app.domain.subscriber.vo_subscriber_id import SubscriberId
from tests.unit.app.application.conftest import MockSubscriberRepository

SUBSCRIBER = "subscriber_id"


class MockTokenGenerator(TokenGenerator):
    def generate(self, input: str) -> str:
        return input

    def validate(self, id: str, token: str):
        return token == id


@pytest.fixture
def token_generator():
    return MockTokenGenerator()


@pytest_asyncio.fixture
async def subscriber_repo():
    repo = MockSubscriberRepository()
    repo._data = {
        SUBSCRIBER: Subscriber(
            id_=SubscriberId(SUBSCRIBER),
            first_name="First",
            last_name="Last",
            phone_number="07123123123",
            email="test@email.com",
            contact_methods=[],
        )
    }
    return repo


@pytest_asyncio.fixture
async def subscriber_service(
    subscriber_repo: SubscriberRepository,
    token_generator: TokenGenerator,
) -> SubscriberService:
    return SubscriberService(
        subscriber_repository=subscriber_repo,
        token_generator=token_generator,
    )


async def test_can_register_subscriber(subscriber_service: SubscriberService) -> None:
    new_id = "new_subscriber_id"
    subscriber = await subscriber_service.register(
        subscriber_id=new_id,
        first_name="test",
        last_name="test",
        contact_methods=[],
    )
    assert isinstance(subscriber, SubscriberDTO)
    repo = subscriber_service._subscriber_repository
    assert await repo.get_by_id(SubscriberId(new_id))


async def test_cannot_register_subscriber_more_than_once(
    subscriber_service: SubscriberService,
) -> None:
    subscriber = await subscriber_service._subscriber_repository.get_by_id(SubscriberId(SUBSCRIBER))
    assert subscriber
    with pytest.raises(SubscriberExistsWithID):
        await subscriber_service.register(
            subscriber_id=SUBSCRIBER,
            first_name="test",
            last_name="test",
            contact_methods=[],
        )


async def test_can_get_subscriber(subscriber_service: SubscriberService) -> None:
    subscriber = await subscriber_service.get(SUBSCRIBER)
    assert isinstance(subscriber, SubscriberDTO)


async def test_cannot_get_non_existent_subscriber(subscriber_service: SubscriberService) -> None:
    with pytest.raises(SubscriberNotFoundById):
        await subscriber_service.get(subscriber_id="test123")
