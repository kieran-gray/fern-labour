from fastapi.security import APIKeyCookie, OAuth2AuthorizationCodeBearer

# Token extraction marker for FastAPI Swagger UI.
# The actual token processing will be handled inside the Identity Provider.
cookie_scheme: APIKeyCookie = APIKeyCookie(name="access_token")

oauth2_scheme: OAuth2AuthorizationCodeBearer = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://localhost:8080/realms/labour_tracker/protocol/openid-connect/auth",
    tokenUrl="http://localhost:8080/realms/labour_tracker/protocol/openid-connect/token",
    refreshUrl="http://localhost:8080/realms/labour_tracker/protocol/openid-connect/token",
)
