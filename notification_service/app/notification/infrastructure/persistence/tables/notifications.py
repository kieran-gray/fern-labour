import json
import logging
import os
from typing import Any

from sqlalchemy import Column, Enum, String, Table
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID
from sqlalchemy.sql import func
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from app.common.infrastructure.persistence.orm_registry import mapper_registry
from app.notification.domain.enums import NotificationStatus, NotificationType

log = logging.getLogger(__name__)


class JSONEncryptedType(StringEncryptedType):  # type: ignore
    def process_result_value(self, value: Any, _: Any) -> Any:
        if value is None:
            return None

        try:
            self._update_key()
            decrypted_value = self.engine.decrypt(value)
        except Exception as e:
            log.error(f"Decryption error: {e}")
            return None

        if isinstance(decrypted_value, dict):
            return decrypted_value

        if isinstance(decrypted_value, str):
            try:
                return json.loads(decrypted_value)
            except json.JSONDecodeError:
                log.error(f"Failed to parse value: {decrypted_value}")
                return None

        return None

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if isinstance(value, dict):
            value = json.dumps(value)
        return super().process_bind_param(value, dialect)


notifications_table = Table(
    "notifications",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("status", Enum(NotificationStatus, name="notification_status"), nullable=False),
    Column("type", Enum(NotificationType, name="notification_type"), nullable=False),
    Column("destination", String, nullable=False),
    Column("template", String, nullable=False),
    Column(
        "data",
        JSONEncryptedType(
            type_in=JSONB,
            key=os.getenv("DATABASE_ENCRYPTION_KEY"),  # TODO dependency injection
            engine=AesEngine,
            padding="pkcs5",
        ),
        nullable=False,
    ),
    Column("metadata", JSONB, nullable=True),
    Column("external_id", String, nullable=True),
    Column("created_at", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
)
