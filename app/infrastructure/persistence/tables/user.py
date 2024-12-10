from sqlalchemy import ARRAY, UUID, Boolean, Column, Enum, LargeBinary, String, Table, event, ExecutionContext, DateTime, text
from sqlalchemy.ext.mutable import MutableSet

from app.domain.constants.user import USERNAME_MAX_LEN
from app.domain.entities.user import UserRoleEnum, User
from app.infrastructure.persistence.orm_registry import mapper_registry

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("username", String(USERNAME_MAX_LEN), nullable=False, unique=True),
    Column("password_hash", LargeBinary, nullable=False),
    Column(
        "roles",
        MutableSet.as_mutable(ARRAY(Enum(UserRoleEnum))),
        default=[UserRoleEnum.USER],
        nullable=False,
    ),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP")),
)


@event.listens_for(User, "load")
def receive_load(target: User, _: ExecutionContext) -> None:
    target.roles = set(target.roles) if isinstance(target.roles, list) else target.roles
