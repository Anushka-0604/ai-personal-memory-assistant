"""add retrieval logs table

Revision ID: 1f9b08126f2a
Revises: 4a6ad9123071
Create Date: 2026-08-22 00:47:42.312888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1f9b08126f2a"
down_revision: Union[str, Sequence[str], None] = "4a6ad9123071"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "retrieval_logs",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "chat_session_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "query",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "retrieved_count",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "selected_count",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "average_similarity",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "retrieval_time_ms",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["chat_session_id"],
            ["chat_sessions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_retrieval_logs_id"),
        "retrieval_logs",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_retrieval_logs_id"),
        table_name="retrieval_logs",
    )

    op.drop_table("retrieval_logs")