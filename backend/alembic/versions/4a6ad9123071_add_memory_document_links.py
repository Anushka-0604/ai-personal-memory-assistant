"""add memory document links

Revision ID: 4a6ad9123071
Revises: 8002c32a5ef0
Create Date: 2026-08-16 21:10:26.152374

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4a6ad9123071"
down_revision: Union[str, Sequence[str], None] = "8002c32a5ef0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "memory_documents",
        sa.Column(
            "memory_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "document_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["documents.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["memory_id"],
            ["memories.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "memory_id",
            "document_id",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("memory_documents")