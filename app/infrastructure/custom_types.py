from dataclasses import dataclass
from typing import Literal, NewType

# security.keycloak
JwtAlgorithm = Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]

# logging
LoggingLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# postgres
PostgresDsn = NewType("PostgresDsn", str)


@dataclass
class AuthScheme:
    server_url: str
    realm: str
    client_id: str
    client_secret: str


@dataclass
class OAuth2Scheme:
    authorizationUrl: str
    tokenUrl: str
    refreshUrl: str


@dataclass
class KeycloakUser:
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    realm_roles: list[str]
    client_roles: list[str]
