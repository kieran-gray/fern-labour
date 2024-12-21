from pathlib import Path
from typing import Any

import pytest

from app.setup.readers.abstract import ConfigReader


class MockConfigReader(ConfigReader):
    def read(self, path: Path) -> dict[str, Any]:
        return {
            "security": {
                "cookies": {
                    "SECURE": 0,
                },
                "cors": {
                    "BACKEND_CORS_ORIGINS": "http://localhost",
                },
                "keycloak": {
                    "KEYCLOAK_SERVER_URL": "http://localhost",
                    "KEYCLOAK_REALM": "test",
                    "KEYCLOAK_CLIENT_ID": "test_client",
                    "KEYCLOAK_CLIENT_SECRET": "ABC123",
                    "JWT_ALGORITHM": "RS256",
                },
            },
            "logging": {
                "LOG_LEVEL": "WARNING",
            },
            "uvicorn": {
                "UVICORN_HOST": "test_host",
                "UVICORN_PORT": 1234,
                "UVICORN_RELOAD": True,
            },
            "db": {
                "postgres": {
                    "POSTGRES_USER": "test_user",
                    "POSTGRES_PASSWORD": "test_password",
                    "POSTGRES_HOST": "test_host",
                    "POSTGRES_PORT": 1234,
                    "POSTGRES_DB": "test_db",
                },
                "sqla_engine": {
                    "SQLA_ECHO": True,
                    "SQLA_ECHO_POOL": False,
                    "SQLA_POOL_SIZE": 1,
                    "SQLA_MAX_OVERFLOW": 0,
                },
            },
        }


@pytest.fixture
def mock_config_reader() -> MockConfigReader:
    return MockConfigReader()
