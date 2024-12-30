from dataclasses import dataclass


@dataclass
class User:
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str | None = None


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
