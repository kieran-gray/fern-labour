"""create metadata column

Revision ID: 9c20dc3c22cc
Revises: 39b6ef13aecf
Create Date: 2025-04-09 20:04:18.766997

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "9c20dc3c22cc"
down_revision: str | None = "39b6ef13aecf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "notifications",
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )

    conn = op.get_bind()
    conn.execute(
        sa.text("""
        UPDATE notifications
        SET metadata = jsonb_strip_nulls(jsonb_build_object(
            'labour_id', labour_id,
            'labour_update_id', labour_update_id,
            'to_user_id', to_user_id,
            'from_user_id', from_user_id
        ))
        """)
    )

    sa.Enum("EMAIL", "SMS", name="notification_type").create(op.get_bind(), checkfirst=True)
    op.execute("""
        ALTER TABLE notifications
        ALTER COLUMN type TYPE notification_type
        USING type::text::notification_type
    """)
    sa.Enum("EMAIL", "SMS", name="contact_method").drop(op.get_bind(), checkfirst=True)

    op.drop_constraint(
        "fk_notifications_labour_update_id_labour_updates", "notifications", type_="foreignkey"
    )
    op.drop_constraint("fk_notifications_labour_id_labours", "notifications", type_="foreignkey")
    op.drop_column("notifications", "labour_update_id")
    op.drop_column("notifications", "labour_id")
    op.drop_column("notifications", "to_user_id")
    op.drop_column("notifications", "from_user_id")


def downgrade() -> None:
    op.add_column("notifications", sa.Column("from_user_id", sa.String(), nullable=True))
    op.add_column("notifications", sa.Column("to_user_id", sa.String(), nullable=True))
    op.add_column("notifications", sa.Column("labour_update_id", sa.UUID(), nullable=True))
    op.add_column("notifications", sa.Column("labour_id", sa.UUID(), nullable=True))

    conn = op.get_bind()
    conn.execute(
        sa.text("""
        UPDATE notifications
        SET
            labour_id = NULLIF(metadata->>'labour_id', '')::uuid,
            labour_update_id = NULLIF(metadata->>'labour_update_id', '')::uuid,
            to_user_id = NULLIF(metadata->>'to_user_id', ''),
            from_user_id = NULLIF(metadata->>'from_user_id', '')
        WHERE metadata IS NOT NULL
        """)
    )

    op.create_foreign_key(
        "fk_notifications_labour_id_labours", "notifications", "labours", ["labour_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_notifications_labour_update_id_labour_updates",
        "notifications",
        "labour_updates",
        ["labour_update_id"],
        ["id"],
    )

    sa.Enum("EMAIL", "SMS", name="contact_method").create(op.get_bind(), checkfirst=True)
    op.execute("""
        ALTER TABLE notifications
        ALTER COLUMN type TYPE contact_method
        USING type::text::contact_method
    """)
    sa.Enum("EMAIL", "SMS", name="notification_type").drop(op.get_bind(), checkfirst=True)

    op.drop_column("notifications", "metadata")
