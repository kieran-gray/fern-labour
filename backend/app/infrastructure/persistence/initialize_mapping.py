__all__ = ("labour", "subscription", "notification")
# When adding new mappings, ensure you add to top of file ^

from app.infrastructure.persistence.mappings import notification, subscription
from app.labour.infrastructure.persistence.mappings import labour
