import pytest_asyncio

from app.application.events.event_handlers.contraction_ended_event_handler import (
    ContractionEndedEventHandler,
)
from app.application.notifications.notification_service import NotificationService
from app.application.services.birthing_person_service import BirthingPersonService
from app.application.services.labour_service import LabourService
from app.application.services.subscriber_service import SubscriberService
from app.domain.labour.constants import (
    CONTRACTIONS_REQUIRED_NULLIPAROUS,
    CONTRACTIONS_REQUIRED_PAROUS,
    LENGTH_OF_CONTRACTIONS_MINUTES,
    TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
    TIME_BETWEEN_CONTRACTIONS_PAROUS,
)
from app.domain.labour.repository import LabourRepository
from tests.unit.app.conftest import get_contractions

BIRTHING_PERSON = "test_birthing_person_id"
SUBSCRIBER = "test_subscriber_id"


@pytest_asyncio.fixture
async def contraction_ended_event_handler(
    labour_repo: LabourRepository,
    birthing_person_service: BirthingPersonService,
    subscriber_service: SubscriberService,
    notification_service: NotificationService,
) -> ContractionEndedEventHandler:
    await birthing_person_service.register(
        birthing_person_id=BIRTHING_PERSON,
        first_name="user",
        last_name="name",
    )
    return ContractionEndedEventHandler(
        labour_repository=labour_repo,
        birthing_person_service=birthing_person_service,
        subscriber_service=subscriber_service,
        notification_service=notification_service,
    )


async def setup_test_data(
    labour_service: LabourService, first_labour: bool = True, should_go_to_hospital: bool = True
):
    labour = await labour_service.begin_labour(BIRTHING_PERSON, True)
    contractions = []
    if not should_go_to_hospital:
        return labour

    if first_labour:
        contractions = get_contractions(
            labour_id=labour.id,
            number_of_contractions=CONTRACTIONS_REQUIRED_NULLIPAROUS,
            length_of_contractions=LENGTH_OF_CONTRACTIONS_MINUTES,
            time_between_contractions=TIME_BETWEEN_CONTRACTIONS_NULLIPAROUS,
        )
    else:
        contractions = get_contractions(
            labour_id=labour.id,
            number_of_contractions=CONTRACTIONS_REQUIRED_PAROUS,
            length_of_contractions=LENGTH_OF_CONTRACTIONS_MINUTES,
            time_between_contractions=TIME_BETWEEN_CONTRACTIONS_PAROUS,
        )
    labour.contractions = contractions
    await labour_service._labour_repository.save(labour)
    return labour


# TODO test setup fixtures need to share repository with event handler

# async def add_subscriber_to_birthing_person(
#     birthing_person_service: BirthingPersonService, birthing_person_id: str, subscriber_id: str
# ) -> None:
#     birthing_person_repo = birthing_person_service._birthing_person_repository
#     birthing_person = await birthing_person_repo.get_by_id(BirthingPersonId(birthing_person_id))
#     birthing_person.subscribers.append(SubscriberId(subscriber_id))
#     await birthing_person_repo.save(birthing_person)


# async def test_contraction_ended_event_no_subscribers(
#     labour_service: LabourService,
#     contraction_ended_event_handler: ContractionEndedEventHandler,
# ) -> None:
#     labour = await setup_test_data(labour_service, True, False)
#     event = DomainEvent(
#         id="event_id",
#         type="contraction.ended",
#         data={"labour_id": labour.id},
#         time=datetime.now(UTC),
#     )
#     await contraction_ended_event_handler.handle(event.to_dict())
#     assert (
#         contraction_ended_event_handler._notification_service._email_notification_gateway.sent_notifications
#         == []
#     )
#     assert (
#         contraction_ended_event_handler._notification_service._sms_notification_gateway.sent_notifications
#         == []
#     )


# async def test_contraction_ended_event_non_existent_labour_id(
#     contraction_ended_event_handler: ContractionEndedEventHandler,
# ) -> None:
#     event = DomainEvent(
#         id="event_id",
#         type="contraction.ended",
#         data={"labour_id": "TEST"},
#         time=datetime.now(UTC),
#     )
#     with pytest.raises(BirthingPersonNotFoundById):
#         await contraction_ended_event_handler.handle(event.to_dict())


# async def test_contraction_ended_event_non_existent_subscriber(
#     contraction_ended_event_handler: ContractionEndedEventHandler,
# ) -> None:
#     await add_subscriber_to_birthing_person(
#         birthing_person_service=contraction_ended_event_handler._birthing_person_service,
#         birthing_person_id=BIRTHING_PERSON,
#         subscriber_id="TEST",
#     )

#     event = DomainEvent(
#         id="event_id",
#         type="contraction.ended",
#         data={"labour_id": BIRTHING_PERSON},
#         time=datetime.now(UTC),
#     )
#     with pytest.raises(SubscriberNotFoundById):
#         await contraction_ended_event_handler.handle(event.to_dict())


# async def test_contraction_ended_event_has_subscriber_no_contact_methods(
#     contraction_ended_event_handler: ContractionEndedEventHandler,
# ) -> None:
#     await contraction_ended_event_handler._subscriber_service.register(
#         subscriber_id=SUBSCRIBER, first_name="test", last_name="test", contact_methods=[]
#     )
#     await add_subscriber_to_birthing_person(
#         birthing_person_service=contraction_ended_event_handler._birthing_person_service,
#         birthing_person_id=BIRTHING_PERSON,
#         subscriber_id=SUBSCRIBER,
#     )

#     event = DomainEvent(
#         id="event_id",
#         type="contraction.ended",
#         data={"labour_id": BIRTHING_PERSON},
#         time=datetime.now(UTC),
#     )
#     await contraction_ended_event_handler.handle(event.to_dict())
#     assert (
#         contraction_ended_event_handler._notification_service._email_notification_gateway.sent_notifications
#         == []
#     )
#     assert (
#         contraction_ended_event_handler._notification_service._sms_notification_gateway.sent_notifications
#         == []
#     )


# async def test_contraction_ended_event_has_subscriber_email(
#     contraction_ended_event_handler: ContractionEndedEventHandler,
# ) -> None:
#     await contraction_ended_event_handler._subscriber_service.register(
#         subscriber_id=SUBSCRIBER,
#         first_name="test",
#         last_name="test",
#         contact_methods=["email"],
#         email="test@email.com",
#     )
#     await add_subscriber_to_birthing_person(
#         birthing_person_service=contraction_ended_event_handler._birthing_person_service,
#         birthing_person_id=BIRTHING_PERSON,
#         subscriber_id=SUBSCRIBER,
#     )

#     event = DomainEvent(
#         id="event_id",
#         type="contraction.ended",
#         data={"labour_id": BIRTHING_PERSON},
#         time=datetime.now(UTC),
#     )
#     await contraction_ended_event_handler.handle(event.to_dict())
#     assert (
#         contraction_ended_event_handler._notification_service._email_notification_gateway.sent_notifications
#         != []
#     )
#     assert (
#         contraction_ended_event_handler._notification_service._sms_notification_gateway.sent_notifications
#         == []
#     )


# async def test_contraction_ended_event_has_subscriber_sms(
#     contraction_ended_event_handler: ContractionEndedEventHandler,
# ) -> None:
#     await contraction_ended_event_handler._subscriber_service.register(
#         subscriber_id=SUBSCRIBER,
#         first_name="test",
#         last_name="test",
#         contact_methods=["sms"],
#         phone_number="07123123123",
#     )
#     await add_subscriber_to_birthing_person(
#         birthing_person_service=contraction_ended_event_handler._birthing_person_service,
#         birthing_person_id=BIRTHING_PERSON,
#         subscriber_id=SUBSCRIBER,
#     )

#     event = DomainEvent(
#         id="event_id",
#         type="contraction.ended",
#         data={"labour_id": BIRTHING_PERSON},
#         time=datetime.now(UTC),
#     )
#     await contraction_ended_event_handler.handle(event.to_dict())
#     assert (
#         contraction_ended_event_handler._notification_service._email_notification_gateway.sent_notifications
#         == []
#     )
#     assert (
#         contraction_ended_event_handler._notification_service._sms_notification_gateway.sent_notifications
#         != []
#     )


# async def test_contraction_ended_event_has_subscriber_all_contact_methods(
#     contraction_ended_event_handler: ContractionEndedEventHandler,
# ) -> None:
#     await contraction_ended_event_handler._subscriber_service.register(
#         subscriber_id=SUBSCRIBER,
#         first_name="test",
#         last_name="test",
#         contact_methods=["sms", "email"],
#         email="test@email.com",
#         phone_number="07123123123",
#     )
#     await add_subscriber_to_birthing_person(
#         birthing_person_service=contraction_ended_event_handler._birthing_person_service,
#         birthing_person_id=BIRTHING_PERSON,
#         subscriber_id=SUBSCRIBER,
#     )

#     event = DomainEvent(
#         id="event_id",
#         type="contraction.ended",
#         data={"labour_id": BIRTHING_PERSON},
#         time=datetime.now(UTC),
#     )
#     await contraction_ended_event_handler.handle(event.to_dict())
#     assert (
#         contraction_ended_event_handler._notification_service._email_notification_gateway.sent_notifications
#         != []
#     )
#     assert (
#         contraction_ended_event_handler._notification_service._sms_notification_gateway.sent_notifications
#         != []
#     )


# async def test_contraction_ended_event_has_subscriber_all_contact_methods_no_phone_number_or_email(
#     contraction_ended_event_handler: ContractionEndedEventHandler,
# ) -> None:
#     await contraction_ended_event_handler._subscriber_service.register(
#         subscriber_id=SUBSCRIBER,
#         first_name="test",
#         last_name="test",
#         contact_methods=["sms", "email"],
#     )
#     await add_subscriber_to_birthing_person(
#         birthing_person_service=contraction_ended_event_handler._birthing_person_service,
#         birthing_person_id=BIRTHING_PERSON,
#         subscriber_id=SUBSCRIBER,
#     )

#     event = DomainEvent(
#         id="event_id",
#         type="contraction.ended",
#         data={"labour_id": BIRTHING_PERSON},
#         time=datetime.now(UTC),
#     )
#     await contraction_ended_event_handler.handle(event.to_dict())
#     assert (
#         contraction_ended_event_handler._notification_service._email_notification_gateway.sent_notifications
#         == []
#     )
#     assert (
#         contraction_ended_event_handler._notification_service._sms_notification_gateway.sent_notifications
#         == []
#     )
