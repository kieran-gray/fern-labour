from dataclasses import dataclass
from datetime import datetime

from app.domain.user.vo_user import UserId


@dataclass(eq=False, kw_only=True)
class SessionRecord:
    id_: str
    user_id: UserId
    expiration: datetime
