from dataclasses import dataclass

from app.common.domain.entity import Entity
from app.user.domain.value_objects.user_id import UserId


@dataclass(eq=False, kw_only=True)
class User(Entity[UserId]):
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str | None = None
