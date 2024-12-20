from sqlalchemy.orm import composite, relationship

from app.domain.birthing_person.entity import BirthingPerson
from app.domain.birthing_person.vo_birthing_person_id import UserId
from app.domain.entities.user_session import UserSession
from app.domain.value_objects.user_password_hash import UserPasswordHash
from app.domain.value_objects.user_username import Username
from app.infrastructure.persistence.orm_registry import mapper_registry
from app.infrastructure.persistence.tables.user import users_table
from app.infrastructure.persistence.tables.user_session import user_sessions_table

mapper_registry.map_imperatively(
    UserSession,
    user_sessions_table,
    properties={
        "id_": user_sessions_table.c.id,
        "user_id": composite(UserId, user_sessions_table.c.user_id),
        "expiration": user_sessions_table.c.expiration,
    },
    column_prefix="_",
)

mapper_registry.map_imperatively(
    BirthingPerson,
    users_table,
    properties={
        "id_": composite(UserId, users_table.c.id),
        "username": composite(Username, users_table.c.username),
        "password_hash": composite(UserPasswordHash, users_table.c.password_hash),
        "sessions": relationship(
            UserSession, back_populates="user", cascade="all", passive_deletes=True
        ),
        "roles": users_table.c.roles,
        "is_active": users_table.c.is_active,
        "created_at": users_table.c.created_at,
    },
    column_prefix="_",
)
