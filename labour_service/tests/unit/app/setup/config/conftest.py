from pathlib import Path
from typing import Any

import pytest

from src.setup.readers.abstract import ConfigReader


class MockConfigReader(ConfigReader):
    def read(self, path: Path) -> dict[str, Any]:
        return {
            "base": {"ENVIRONMENT": "test", "SUPPORT_EMAIL": "test@email.com"},
            "security": {
                "cors": {
                    "BACKEND_CORS_ORIGINS": "http://localhost,https://localhost",
                    "FRONTEND_HOST": "http://localhost:1234",
                    "MARKETING_HOST": "http://localhost:3000",
                },
                "keycloak": {
                    "KEYCLOAK_SERVER_URL": "http://localhost",
                    "KEYCLOAK_REALM": "test",
                    "KEYCLOAK_CLIENT_ID": "test_client",
                    "KEYCLOAK_CLIENT_SECRET": "ABC123",
                    "KEYCLOAK_ADMIN": "user",
                    "KEYCLOAK_ADMIN_PASSWORD": "pass",
                    "JWT_ALGORITHM": "RS256",
                },
                "subscriber_token": {
                    "SUBSCRIBER_TOKEN_SALT": "salty",
                },
                "cloudflare": {
                    "CLOUDFLARE_URL": "test",
                    "CLOUDFLARE_SECRET_KEY": "secret",
                },
                "rate_limits": {
                    "LABOUR_INVITE_RATE_LIMIT": 20,
                    "LABOUR_INVITE_RATE_LIMIT_EXPIRY": 86400,
                    "SUBSCRIBER_INVITE_RATE_LIMIT": 20,
                    "SUBSCRIBER_INVITE_RATE_LIMIT_EXPIRY": 86400,
                }
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
            "notifications": {
                "email": {
                    "SUPPORT_EMAIL": "support@example.com",
                    "TRACKING_LINK": "http://test.com",
                },
                "twilio": {},
            },
            "events": {
                "gcp": {"GCP_PROJECT_ID": "test"},
            },
            "payments": {
                "stripe": {"STRIPE_API_KEY": "test", "STRIPE_WEBHOOK_ENDPOINT_SECRET": "test"}
            },
            "redis": {
                "REDIS_HOST": "localhost",
                "REDIS_PORT": 1234,
                "REDIS_PASSWORD": "password",
            }
        }


@pytest.fixture
def mock_config_reader() -> MockConfigReader:
    return MockConfigReader()
