__all__ = ("labour", "subscription", "notification")
# When adding new mappings, ensure you add to top of file ^

from app.labour.infrastructure.persistence.mappings import labour
from app.notification.infrastructure.persistence.mappings import notification
from app.subscription.infrastructure.persistence.mappings import subscription
