from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.value_objects.user_id import UserId


@dataclass(kw_only=True)
class UserSession:
    id_: UUID
    user_id: UserId
    expiration: datetime
