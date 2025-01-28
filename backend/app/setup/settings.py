import logging
import os
from pathlib import Path
from typing import Any, Literal, Self

from pydantic import BaseModel, Field, PostgresDsn, computed_field

from app.setup.constants import BASE_DIR
from app.setup.readers.abstract import ConfigReader
from app.setup.readers.toml import TomlConfigReader

log = logging.getLogger(__name__)


class KeycloakSettings(BaseModel):
    server_url: str = Field(alias="KEYCLOAK_SERVER_URL")
    docker_url: str | None = Field(alias="KEYCLOAK_DOCKER_URL", default=None)
    realm: str = Field(alias="KEYCLOAK_REALM")
    client_id: str = Field(alias="KEYCLOAK_CLIENT_ID")
    client_secret: str = Field(alias="KEYCLOAK_CLIENT_SECRET")
    jwt_algorithm: Literal[
        "HS256",
        "HS384",
        "HS512",
        "RS256",
        "RS384",
        "RS512",
    ] = Field(alias="JWT_ALGORITHM")


class SubscriberTokenSettings(BaseModel):
    salt: str = Field(alias="SUBSCRIBER_TOKEN_SALT")


class CORSSettings(BaseModel):
    backend_cors_origins: str = Field(alias="BACKEND_CORS_ORIGINS")
    frontend_host: str = Field(alias="FRONTEND_HOST")
    marketing_host: str = Field(alias="MARKETING_HOST")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        all_origins = self.backend_cors_origins.split(",") + [self.frontend_host] + [self.marketing_host]
        return [str(origin).rstrip("/") for origin in all_origins]


class SecuritySettings(BaseModel):
    cors: CORSSettings
    keycloak: KeycloakSettings
    subscriber_token: SubscriberTokenSettings


class LoggingSettings(BaseModel):
    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = Field(alias="LOG_LEVEL")


class UvicornSettings(BaseModel):
    host: str = Field(alias="UVICORN_HOST")
    port: int = Field(alias="UVICORN_PORT")
    reload: bool = Field(alias="UVICORN_RELOAD")


class PostgresSettings(BaseModel):
    username: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    path: str = Field(alias="POSTGRES_DB")

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.path,
            )
        )


class SqlaEngineSettings(BaseModel):
    echo: bool = Field(alias="SQLA_ECHO")
    echo_pool: bool = Field(alias="SQLA_ECHO_POOL")
    pool_size: int = Field(alias="SQLA_POOL_SIZE")
    max_overflow: int = Field(alias="SQLA_MAX_OVERFLOW")


class DbSettings(BaseModel):
    postgres: PostgresSettings
    sqla_engine: SqlaEngineSettings


class EmailSettings(BaseModel):
    smtp_host: str | None = Field(alias="SMTP_HOST", default=None)
    smtp_user: str | None = Field(alias="SMTP_USER", default=None)
    smtp_password: str | None = Field(alias="SMTP_PASSWORD", default=None)
    emails_from_email: str | None = Field(alias="EMAILS_FROM_EMAIL", default=None)
    emails_from_name: str | None = Field(alias="EMAILS_FROM_NAME", default=None)
    smtp_tls: bool = Field(alias="SMTP_TLS", default=True)
    smtp_ssl: bool = Field(alias="SMTP_SSL", default=False)
    smtp_port: int = Field(alias="SMTP_PORT", default=587)
    support_email: str | None = Field(alias="SUPPORT_EMAIL", default=None)

    @property
    def emails_enabled(self) -> bool:
        return bool(self.smtp_host and self.smtp_port and self.emails_from_email)


class TwilioSettings(BaseModel):
    account_sid: str | None = Field(alias="TWILIO_ACCOUNT_SID", default=None)
    auth_token: str | None = Field(alias="TWILIO_AUTH_TOKEN", default=None)
    sms_from_number: str | None = Field(alias="SMS_FROM_NUMBER", default=None)

    @property
    def twilio_enabled(self) -> bool:
        return bool(self.account_sid and self.auth_token and self.sms_from_number)


class NotificationSettings(BaseModel):
    email: EmailSettings
    twilio: TwilioSettings


class KafkaSettings(BaseModel):
    bootstrap_servers: str = Field(alias="KAFKA_BOOTSTRAP_SERVERS")
    topic_prefix: str = Field(alias="KAFKA_TOPIC_PREFIX", default="labour-tracker")

    @property
    def kafka_enabled(self) -> bool:
        return bool(self.bootstrap_servers)


class KafkaProducerSettings(BaseModel):
    retries: int = Field(alias="KAFKA_PRODUCER_RETRIES", default=3)
    acks: str = Field(alias="KAFKA_PRODUCER_ACKS", default="all")


class KafkaConsumerSettings(BaseModel):
    group_id: str = Field(alias="KAFKA_GROUP_ID", default="labour-tracker-group")


class EventSettings(BaseModel):
    kafka_producer: KafkaProducerSettings
    kafka_consumer: KafkaConsumerSettings
    kafka: KafkaSettings


class Settings(BaseModel):
    security: SecuritySettings
    logging: LoggingSettings
    uvicorn: UvicornSettings
    notifications: NotificationSettings
    events: EventSettings
    db: DbSettings

    _cfg_toml_path: Path = BASE_DIR / "config.toml"

    @classmethod
    def from_file(
        cls,
        path: Path = _cfg_toml_path,
        reader: ConfigReader = TomlConfigReader(),
        strict: bool = False,
        override: bool = True,
    ) -> Self:
        if not path.is_file():
            raise FileNotFoundError(f"The file does not exist at the specified path: {path}")
        config_data = reader.read(path)
        if override:
            config_data = cls.override_from_env(toml=config_data)
        settings = cls.model_validate(config_data, strict=strict)
        log.debug(f"Settings read from {path=}.")
        return settings

    @classmethod
    def override_from_env(cls, toml: dict[str, Any]) -> dict[str, Any]:
        """Override any values in the config.toml that are set in the environment."""
        for key, value in toml.items():
            if isinstance(value, dict):
                cls.override_from_env(value)
            if value := os.getenv(key):
                toml[key] = value
        return toml
