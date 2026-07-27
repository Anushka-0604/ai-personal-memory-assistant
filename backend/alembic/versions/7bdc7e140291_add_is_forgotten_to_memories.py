"""add is_forgotten to memories

Revision ID: 7bdc7e140291
Revises: c77eac07519e
Create Date: 2026-07-27 23:25:39.513454

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7bdc7e140291"
down_revision: Union[str, Sequence[str], None] = "c77eac07519e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "memories",
        sa.Column(
            "is_forgotten",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "memories",
        "is_forgotten",
    )