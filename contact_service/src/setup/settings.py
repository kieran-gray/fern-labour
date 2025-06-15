import logging
import os
from pathlib import Path
from typing import Any, Literal, Self

from pydantic import BaseModel, Field, PostgresDsn, computed_field

from src.setup.constants import BASE_DIR
from src.setup.readers.abstract import ConfigReader
from src.setup.readers.toml import TomlConfigReader

log = logging.getLogger(__name__)


class BaseSettings(BaseModel):
    environment: str = Field(alias="ENVIRONMENT")
    support_email: str = Field(alias="SUPPORT_EMAIL")


class KeycloakSettings(BaseModel):
    server_url: str = Field(alias="KEYCLOAK_SERVER_URL")
    realm: str = Field(alias="KEYCLOAK_REALM")
    client_id: str = Field(alias="KEYCLOAK_CLIENT_ID")
    client_secret: str = Field(alias="KEYCLOAK_CLIENT_SECRET")


class UserManagementSettings(BaseModel):
    client_id: str = Field(alias="USER_MANAGEMENT_SERVICE_CLIENT_ID")
    client_secret: str = Field(alias="USER_MANAGEMENT_SERVICE_CLIENT_SECRET")


class CORSSettings(BaseModel):
    backend_cors_origins: str = Field(alias="BACKEND_CORS_ORIGINS")
    frontend_host: str = Field(alias="FRONTEND_HOST")
    marketing_host: str = Field(alias="MARKETING_HOST")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        all_origins = (
            self.backend_cors_origins.split(",") + [self.frontend_host] + [self.marketing_host]
        )
        return [str(origin).rstrip("/") for origin in all_origins]


class CloudflareSettings(BaseModel):
    cloudflare_url: str = Field(alias="CLOUDFLARE_URL")
    cloudflare_secret_key: str = Field(alias="CLOUDFLARE_SECRET_KEY")


class SecuritySettings(BaseModel):
    cors: CORSSettings
    keycloak: KeycloakSettings
    cloudflare: CloudflareSettings
    user_management: UserManagementSettings


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


class GCPSettings(BaseModel):
    project_id: str = Field(alias="GCP_PROJECT_ID")
    retries: int = Field(alias="GCP_PRODUCER_RETRIES", default=3)
    consumer_mode: str = Field(alias="GCP_PUB_SUB_CONSUMER_MODE")
    max_batch_size: int = Field(alias="GCP_PUB_SUB_CONSUMER_MAX_BATCH_SIZE")


class EventSettings(BaseModel):
    gcp: GCPSettings


class SlackSettings(BaseModel):
    token: str = Field(alias="SLACK_ALERT_BOT_TOKEN", default="")
    alert_channel: str = Field(alias="SLACK_ALERT_BOT_CHANNEL", default="")

    @property
    def slack_enabled(self) -> bool:
        return bool(self.token and self.alert_channel)


class Settings(BaseModel):
    base: BaseSettings
    security: SecuritySettings
    logging: LoggingSettings
    uvicorn: UvicornSettings
    events: EventSettings
    db: DbSettings
    slack: SlackSettings

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
