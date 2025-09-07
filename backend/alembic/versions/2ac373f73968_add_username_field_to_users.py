"""Add username field to users

Revision ID: 2ac373f73968
Revises: f20a588a77a0
Create Date: 2025-09-07 11:50:08.290518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ac373f73968'
down_revision: Union[str, Sequence[str], None] = 'f20a588a77a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('username', sa.String(length=50), nullable=True))
    op.create_unique_constraint('uq_users_username', 'users', ['username'])
    op.create_index('ix_users_username', 'users', ['username'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_users_username', 'users')
    op.drop_constraint('uq_users_username', 'users')
    op.drop_column('users', 'username')
