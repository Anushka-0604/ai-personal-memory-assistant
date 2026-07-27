"""add evidence_count to memories

Revision ID: 050b5a8bc2b1
Revises: 5f6b6f20c449
Create Date: 2026-07-27 21:30:31.918481

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "050b5a8bc2b1"
down_revision: Union[str, Sequence[str], None] = "5f6b6f20c449"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "memories",
        sa.Column(
            "evidence_count",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "memories",
        "evidence_count",
    )