import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fern_labour_notifications_shared.enums import NotificationTemplate
from fern_labour_notifications_shared.notification_data import BaseNotificationData

from src.notification.application.dtos.notification import NotificationDTO, NotificationSendResult
from src.notification.application.interfaces.notification_gateway import (
    EmailNotificationGateway,
    SMSNotificationGateway,
    WhatsAppNotificationGateway,
)
from src.notification.application.interfaces.template_engine import (
    EmailTemplateEngine,
)
from src.notification.application.interfaces.template_engine import (
    SMSTemplateEngine as SMSTemplateEngineInterface,
)
from src.notification.application.interfaces.template_engine import (
    WhatsAppTemplateEngine as WhatsAppTemplateEngineInterface,
)
from src.notification.application.services.notification_generation_service import (
    NotificationGenerationService,
)
from src.notification.application.services.notification_service import NotificationService
from src.notification.domain.entity import Notification
from src.notification.domain.enums import NotificationStatus
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

    async def save(self, notification: Notification) -> None:
        self._data[notification.id_.value] = notification

    async def delete(self, notification: Notification) -> None:
        self._data.pop(notification.id_.value)

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


@pytest_asyncio.fixture
async def user_repo() -> UserRepository:
    repo = MockUserRepository()
    repo._data = {}
    return repo


@pytest_asyncio.fixture
async def notification_repo() -> NotificationRepository:
    repo = MockNotificationRepository()
    repo._data = {}
    return repo


class MockEmailNotificationGateway(EmailNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(success=True, status=NotificationStatus.SENT)


class MockSMSNotificationGateway(SMSNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(success=True, status=NotificationStatus.SENT)


class MockWhatsAppNotificationGateway(WhatsAppNotificationGateway):
    sent_notifications = []

    async def send(self, data: NotificationDTO) -> NotificationSendResult:
        self.sent_notifications.append(data)
        return NotificationSendResult(success=True, status=NotificationStatus.SENT)


class MockEmailTemplateEngine(EmailTemplateEngine):
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
async def user_service(user_repo: UserRepository) -> UserQueryService:
    return UserQueryService(user_repository=user_repo)


@pytest.fixture
def email_template_engine() -> EmailTemplateEngine:
    return MockEmailTemplateEngine()


@pytest.fixture
def sms_template_engine() -> SMSTemplateEngineInterface:
    return SMSTemplateEngine()


@pytest.fixture
def whatsapp_template_engine() -> WhatsAppTemplateEngineInterface:
    return WhatsAppTemplateEngine()


@pytest_asyncio.fixture
async def notification_generation_service(
    notification_repo: NotificationRepository,
    email_template_engine: EmailTemplateEngine,
    sms_template_engine: SMSTemplateEngine,
    whatsapp_template_engine: WhatsAppTemplateEngine,
) -> NotificationGenerationService:
    return NotificationGenerationService(
        notification_repo=notification_repo,
        email_template_engine=email_template_engine,
        sms_template_engine=sms_template_engine,
        whatsapp_template_engine=whatsapp_template_engine,
    )


@pytest_asyncio.fixture
async def notification_service(
    notification_generation_service: NotificationGenerationService,
    notification_repo: NotificationRepository,
) -> NotificationService:
    email_notification_gateway = MockEmailNotificationGateway()
    sms_notification_gateway = MockSMSNotificationGateway()
    whatsapp_notification_gateway = MockWhatsAppNotificationGateway()
    email_notification_gateway.sent_notifications = []
    sms_notification_gateway.sent_notifications = []
    return NotificationService(
        email_notification_gateway=email_notification_gateway,
        sms_notification_gateway=sms_notification_gateway,
        whatsapp_notification_gateway=whatsapp_notification_gateway,
        notification_generation_service=notification_generation_service,
        notification_repository=notification_repo,
        event_producer=AsyncMock(),
    )
