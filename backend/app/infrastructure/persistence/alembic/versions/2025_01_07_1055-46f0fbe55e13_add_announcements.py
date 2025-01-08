"""add announcements

Revision ID: 46f0fbe55e13
Revises: 9f6cd8626377
Create Date: 2025-01-07 10:55:23.361568

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "46f0fbe55e13"
down_revision: str | None = "9f6cd8626377"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "announcements",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("labour_id", sa.UUID(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("sent_time", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["labour_id"], ["labours.id"], name=op.f("fk_announcements_labour_id_labours")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_announcements")),
    )


def downgrade() -> None:
    op.drop_table("announcements")
