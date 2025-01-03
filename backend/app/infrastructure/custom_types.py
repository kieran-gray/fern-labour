from typing import Literal, NewType

# security.keycloak
JwtAlgorithm = Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]

# logging
LoggingLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# postgres
PostgresDsn = NewType("PostgresDsn", str)
