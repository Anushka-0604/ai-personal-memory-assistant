"""add embedding to document_chunks

Revision ID: 69d1da07cac7
Revises: 6b6d7bdf2a4a
Create Date: 2026-08-04 22:22:32.754594

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "69d1da07cac7"
down_revision: Union[str, Sequence[str], None] = "6b6d7bdf2a4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "document_chunks",
        sa.Column(
            "embedding",
            Vector(384),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "document_chunks",
        "embedding",
    )