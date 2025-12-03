import json
import logging
import os
from typing import Any

from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from src.core.infrastructure.persistence.orm_registry import mapper_registry

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


domain_events_table = Table(
    "domain_events",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event_id", String, nullable=False),
    Column("aggregate_id", String, nullable=False),
    Column("aggregate_type", String, nullable=False),
    Column("type", String, nullable=False),
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
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("published_at", DateTime(timezone=True), nullable=True),
)
