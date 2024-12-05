from uuid import UUID

import uuid6

from app.application.user.ports.user_id_generator import (
    UserIdGeneratorInterface,
)


class UuidUserIdGenerator(UserIdGeneratorInterface):
    def __call__(self) -> UUID:
        return uuid6.uuid7()
