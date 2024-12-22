import logging
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, Field, PostgresDsn, computed_field

from app.setup.constants import BASE_DIR
from app.setup.readers.abstract import ConfigReader
from app.setup.readers.toml import TomlConfigReader

log = logging.getLogger(__name__)


class KeycloakSettings(BaseModel):
    server_url: str = Field(alias="KEYCLOAK_SERVER_URL")
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


class CookiesSettings(BaseModel):
    secure: bool = Field(alias="SECURE")


class CORSSettings(BaseModel):
    BACKEND_CORS_ORIGINS: str = Field(alias="BACKEND_CORS_ORIGINS")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]


class SecuritySettings(BaseModel):
    cookies: CookiesSettings
    cors: CORSSettings
    keycloak: KeycloakSettings


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
    smtp_port: int = Field(alias="SMTP_PORT", default = 587)

    @property
    def emails_enabled(self) -> bool:
        return self.smtp_host and self.emails_from_email


class NotificationSettings(BaseModel):
    email: EmailSettings


class Settings(BaseModel):
    security: SecuritySettings
    logging: LoggingSettings
    uvicorn: UvicornSettings
    notification: NotificationSettings
    db: DbSettings

    _cfg_toml_path: Path = BASE_DIR / "config.toml"

    @classmethod
    def from_file(
        cls,
        path: Path = _cfg_toml_path,
        reader: ConfigReader = TomlConfigReader(),
        strict: bool = False,
    ) -> Self:
        if not path.is_file():
            raise FileNotFoundError(f"The file does not exist at the specified path: {path}")
        config_data = reader.read(path)
        settings = cls.model_validate(config_data, strict=strict)
        log.debug(f"Settings read from {path=}.")
        return settings
