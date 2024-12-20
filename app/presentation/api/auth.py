from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

from app.core.settings import Settings
from app.infrastructure.custom_types import KeycloakUser

settings = Settings.from_file()


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.security.keycloak.server_url}/realms/{settings.security.keycloak.realm}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.security.keycloak.server_url}/realms/{settings.security.keycloak.realm}/protocol/openid-connect/token",
    refreshUrl=f"{settings.security.keycloak.server_url}/realms/{settings.security.keycloak.realm}/protocol/openid-connect/token",
)


keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080",
    realm_name=settings.security.keycloak.realm,
    client_id=settings.security.keycloak.client_id,
    client_secret_key=settings.security.keycloak.client_secret,
    verify=True
)


async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    try:
        return keycloak_openid.decode_token(
            token,
            key=await get_idp_public_key(),
            validate=False,  # WARNING NEEDS TO BE TRUE
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_info(payload: dict = Depends(get_payload)) -> KeycloakUser:
    try:
        return KeycloakUser(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            email=payload.get("email"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
            client_roles=payload.get("realm_access", {}).get("roles", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
