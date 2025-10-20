"""Create phone number for users database

Revision ID: e7bfc348eaa6
Revises: 
Create Date: 2025-10-20 09:58:37.167365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7bfc348eaa6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('phone',sa.String(),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
