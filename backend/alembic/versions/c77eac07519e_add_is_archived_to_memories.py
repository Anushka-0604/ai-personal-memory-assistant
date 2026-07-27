"""add is_archived to memories

Revision ID: c77eac07519e
Revises: 050b5a8bc2b1
Create Date: 2026-07-27 23:17:34.518224

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c77eac07519e"
down_revision: Union[str, Sequence[str], None] = "050b5a8bc2b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "memories",
        sa.Column(
            "is_archived",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "memories",
        "is_archived",
    )