from sqlalchemy import Column, DateTime, String, Table, text

from app.infrastructure.persistence.orm_registry import mapper_registry

birthing_persons_table = Table(
    "birthing_persons",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("phone_number", String, nullable=True),
    Column("email", String, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column(
        "updated_at",
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
)
