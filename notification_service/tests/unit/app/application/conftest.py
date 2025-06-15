from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Self
from unittest.mock import AsyncMock

import pytest_asyncio
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import BaseNotificationData
from fern_labour_core.events.event import DomainEvent
from fern_labour_core.unit_of_work import UnitOfWork

from src.core.application.domain_event_publisher import DomainEventPublisher
from src.core.infrastructure.asyncio_task_manager import AsyncioTaskManager
from src.core.domain.domain_event.repository import DomainEventRepository
from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.interfaces.notification_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
    WhatsAppNotificationGateway,
)
from src.notification.application.interfaces.template_engine import NotificationTemplateEngine
from src.notification.application.services.notification_delivery_service import (
    NotificationDeliveryService,
)
from src.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from src.notification.application.services.notification_router import NotificationRouter
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.entity import Notification
from src.notification.domain.enums import NotificationChannel, NotificationStatus
from src.notification.domain.repository import NotificationRepository
from src.notification.domain.value_objects.notification_id import NotificationId
from src.notification.infrastructure.template_engines.sms_template_engine import SMSTemplateEngine
from src.notification.infrastructure.template_engines.whatsapp_template_engine import (
    WhatsAppTemplateEngine,
)
from src.user.application.services.user_query_service import UserQueryService
from src.user.domain.entity import User
from src.user.domain.repository import UserRepository
from src.user.domain.value_objects.user_id import UserId


class MockUserRepository(UserRepository):
    _data = {}

    async def save(self, user: User) -> None:
        self._data[user.id_.value] = user

    async def delete(self, user: User) -> None:
        self._data.pop(user.id_.value)

    async def get_by_id(self, user_id: UserId) -> User | None:
        return self._data.get(user_id.value, None)

    async def get_by_ids(self, user_ids: list[UserId]) -> list[User]:
        users = []
        for user_id in user_ids:
            if user := self._data.get(user_id.value, None):
                users.append(user)
        return users


class MockNotificationRepository(NotificationRepository):
    _data: dict[str, Notification] = {}
    _changes: dict[str, Notification] = {}


    async def save(self, notification: Notification) -> None:
        self._changes[notification.id_.value] = notification

    async def delete(self, notification: Notification) -> None:
        self._changes.pop(notification.id_.value)

    async def get_by_id(self, notification_id: NotificationId) -> Notification | None:
        return self._data.get(notification_id.value, None)

    async def get_by_ids(self, notification_ids: list[NotificationId]) -> list[Notification]:
        notifications = []
        for notification_id in notification_ids:
            if notification := self._data.get(notification_id.value, None):
                notifications.append(notification)
        return notifications

    async def get_by_external_id(self, external_id: str):
        return next(
            (
                notification
                for notification in self._data.values()
                if notification.external_id == external_id
            ),
            None,
        )

    async def get_by_external_ids(self, external_ids):
        return await super().get_by_external_ids(external_ids)

    async def get_undelivered_notifications(self):
        def check(notification: Notification) -> bool:
            return bool(
                notification.status is NotificationStatus.SENT
                and notification.external_id is not None
            )

        return [notification for notification in self._data.values() if check(notification)]


class MockDomainEventRepository(DomainEventRepository):
    _data: dict[str, tuple[DomainEvent, datetime | None]] = {}
    _changes: dict[str, tuple[DomainEvent, datetime | None]] = {}

    async def commit(self) -> None:
        self._data.update(self._changes)

    async def save(self, domain_event: DomainEvent) -> None:
        self._changes[domain_event.id] = (domain_event, None)

    async def save_many(self, domain_events: list[DomainEvent]):
        for domain_event in domain_events:
            self._changes[domain_event.id] = (domain_event, None)

    async def get_unpublished(self, limit=100) -> list[DomainEvent]:
        unpublished = []
        for domain_event, published in self._changes.values():
            if not published:
                unpublished.append(domain_event)
        return unpublished

    async def mark_as_published(self, domain_event_id: str) -> None:
        domain_event = self._changes.get(domain_event_id)
        domain_event[1] = datetime.now(UTC)

    async def mark_many_as_published(self, domain_event_ids: list[str]) -> None:
        for domain_event_id in domain_event_ids:
            self.mark_as_published(domain_event_id)


@pytest_asyncio.fixture
async def user_repo() -> UserRepository:
    repo = MockUserRepository()
    repo._data = {}
    return repo


@pytest_asyncio.fixture
async def notification_repo() -> NotificationRepository:
    repo = MockNotificationRepository()
    repo._data = {}
    repo._changes = {}
    return repo


@pytest_asyncio.fixture
async def domain_event_repo() -> DomainEventRepository:
    repo = MockDomainEventRepository()
    repo._data = {}
    repo._changes = {}
    return repo


class MockUnitOfWork(UnitOfWork):
    def __init__(self, repositories) -> None:
        self._repositories: list = repositories

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        except Exception:
            raise
        return None

    async def commit(self) -> None:
        for repository in self._repositories:
            repository._data.update(repository._changes)

    async def rollback(self) -> None:
        for repository in self._repositories:
            repository._changes = {}


@pytest_asyncio.fixture
async def unit_of_work(
    domain_event_repo: DomainEventRepository,
    notification_repo: NotificationRepository,
) -> UnitOfWork:
    return MockUnitOfWork(repositories=[domain_event_repo, notification_repo])


class MockEmailNotificationGateway(EmailNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(
            success=True, status=NotificationStatus.SENT, external_id="TESTEMAIL"
        )

    async def get_status(self, external_id: str) -> str:
        raise NotImplementedError()

    async def redact_notification_body(self, external_id: str) -> None:
        raise NotImplementedError()


class MockSMSNotificationGateway(SMSNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(
            success=True, status=NotificationStatus.SENT, external_id="TESTSMS"
        )

    async def get_status(self, external_id: str) -> str | None:
        return NotificationStatus.SUCCESS

    async def redact_notification_body(self, external_id: str) -> None:
        return None


class MockWhatsAppNotificationGateway(WhatsAppNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(
            success=True, status=NotificationStatus.SENT, external_id="TESTWHATSAPP"
        )

    async def get_status(self, external_id: str) -> str | None:
        return NotificationStatus.SENT

    async def redact_notification_body(self, external_id: str) -> None:
        return None


class MockEmailTemplateEngine(NotificationTemplateEngine):
    directory = Path()

    def generate_subject(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        return f"Mock HTML subject: {template_name} {json.dumps(data.to_dict())}"

    def generate_message(
        self, template_name: NotificationTemplate, data: BaseNotificationData
    ) -> str:
        return f"Mock HTML email: {template_name} {json.dumps(data.to_dict())}"
    

@pytest_asyncio.fixture
async def domain_event_publisher(
    domain_event_repo: DomainEventRepository, unit_of_work: UnitOfWork
) -> DomainEventPublisher:
    return DomainEventPublisher(
        domain_event_repository=domain_event_repo,
        unit_of_work=unit_of_work,
        event_producer=AsyncMock(),
        task_manager=AsyncioTaskManager(),
    )


@pytest_asyncio.fixture
async def user_service(user_repo: UserRepository) -> UserQueryService:
    return UserQueryService(user_repository=user_repo)


@pytest_asyncio.fixture
async def notification_generation_service(
    notification_repo: NotificationRepository,
) -> NotificationGenerationService:
    notification_generation_service = NotificationGenerationService(
        notification_repo=notification_repo,
    )
    notification_generation_service.register_template_engine(
        channel=NotificationChannel.EMAIL, template_engine=MockEmailTemplateEngine()
    )
    notification_generation_service.register_template_engine(
        channel=NotificationChannel.SMS, template_engine=SMSTemplateEngine()
    )
    notification_generation_service.register_template_engine(
        channel=NotificationChannel.WHATSAPP, template_engine=WhatsAppTemplateEngine()
    )
    return notification_generation_service


@pytest_asyncio.fixture
async def notification_router(
    email_notification_gateway=MockEmailNotificationGateway(),
    sms_notification_gateway=MockSMSNotificationGateway(),
    whatsapp_notification_gateway=MockWhatsAppNotificationGateway(),
) -> NotificationRouter:
    email_notification_gateway.sent_notifications = []
    sms_notification_gateway.sent_notifications = []
    whatsapp_notification_gateway.sent_notifications = []
    router = NotificationRouter()
    router.register_gateway(NotificationChannel.EMAIL, email_notification_gateway)
    router.register_gateway(NotificationChannel.SMS, sms_notification_gateway)
    router.register_gateway(NotificationChannel.WHATSAPP, whatsapp_notification_gateway)
    return router


@pytest_asyncio.fixture
async def notification_service(
    notification_generation_service: NotificationGenerationService,
    notification_repo: NotificationRepository,
    notification_router: NotificationRouter,
    domain_event_repo: DomainEventRepository,
    domain_event_publisher: DomainEventPublisher,
    unit_of_work: UnitOfWork,
) -> NotificationService:
    return NotificationService(
        notification_router=notification_router,
        notification_generation_service=notification_generation_service,
        notification_repository=notification_repo,
        domain_event_repository=domain_event_repo,
        domain_event_publisher=domain_event_publisher,
        unit_of_work=unit_of_work
    )


@pytest_asyncio.fixture
async def notification_delivery_service(
    notification_service: NotificationService,
    notification_repo: NotificationRepository,
    notification_router: NotificationRouter,
    domain_event_repo: DomainEventRepository,
    domain_event_publisher: DomainEventPublisher,
    unit_of_work: UnitOfWork,
) -> NotificationDeliveryService:
    return NotificationDeliveryService(
        notification_service=notification_service,
        notification_router=notification_router,
        notification_repository=notification_repo,
        domain_event_repository=domain_event_repo,
        domain_event_publisher=domain_event_publisher,
        unit_of_work=unit_of_work
    )
