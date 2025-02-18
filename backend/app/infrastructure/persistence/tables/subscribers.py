from sqlalchemy import Column, String, Table

from app.infrastructure.persistence.orm_registry import mapper_registry

subscribers_table = Table(
    "subscribers",
    mapper_registry.metadata,
    Column("id", String, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("phone_number", String, nullable=True),
    Column("email", String, nullable=True),
)
