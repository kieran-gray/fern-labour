from pathlib import Path

import pytest
from pydantic import PostgresDsn, ValidationError

from app.setup.readers.abstract import ConfigReader
from app.setup.settings import LoggingSettings, Settings


def test_settings_from_file(mock_config_reader: ConfigReader, tmp_path: Path):
    fake_path: Path = tmp_path / "test_config.toml"
    fake_path.touch()
    settings: Settings = Settings.from_file(
        path=fake_path, reader=mock_config_reader, override=False
    )

    assert settings.logging.level == "WARNING"

    assert settings.uvicorn.host == "test_host"
    assert settings.uvicorn.port == 1234
    assert settings.uvicorn.reload is True

    assert settings.security.cors.all_cors_origins == [
        "http://localhost",
        "https://localhost",
        "http://localhost:1234",
        "http://localhost:3000",
    ]

    assert settings.db.postgres.username == "test_user"
    assert settings.db.postgres.password == "test_password"
    assert settings.db.postgres.host == "test_host"
    assert settings.db.postgres.port == 1234
    assert settings.db.postgres.path == "test_db"

    assert settings.db.postgres.dsn == str(
        PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=settings.db.postgres.username,
            password=settings.db.postgres.password,
            host=settings.db.postgres.host,
            port=settings.db.postgres.port,
            path=settings.db.postgres.path,
        )
    )

    assert settings.db.sqla_engine.echo is True
    assert settings.db.sqla_engine.echo_pool is False
    assert settings.db.sqla_engine.pool_size == 1
    assert settings.db.sqla_engine.max_overflow == 0

    assert settings.notifications.email.emails_enabled is False
    assert settings.notifications.twilio.twilio_enabled is False

    assert settings.events.kafka.kafka_enabled is True

    assert settings.payments.stripe.stripe_enabled is True


def test_settings_from_file_not_found(mock_config_reader: ConfigReader):
    fake_path: Path = Path("fake_path")

    with pytest.raises(FileNotFoundError):
        Settings.from_file(fake_path, mock_config_reader)


def test_settings_with_env_variables(monkeypatch, mock_config_reader: ConfigReader, tmp_path: Path):
    monkeypatch.setenv("UVICORN_HOST", "127.0.0.1")
    monkeypatch.setenv("UVICORN_PORT", "9999")

    fake_path: Path = tmp_path / "test_config.toml"
    fake_path.touch()

    settings: Settings = Settings.from_file(path=fake_path, reader=mock_config_reader)

    assert settings.uvicorn.host == "127.0.0.1"
    assert settings.uvicorn.port == 9999


def test_logging_settings_validation():
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        LoggingSettings(LOG_LEVEL=level)  # type: ignore

    with pytest.raises(ValidationError):
        LoggingSettings(LOG_LEVEL="INVALID_LEVEL")  # type: ignore
