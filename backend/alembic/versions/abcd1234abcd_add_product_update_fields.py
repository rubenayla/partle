"""add product modification tracking

Revision ID: abcd1234abcd
Revises: 0d106763b960
Create Date: 2025-06-21 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'abcd1234abcd'
down_revision: Union[str, Sequence[str], None] = '0d106763b960'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('products', sa.Column('updated_by_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'products', 'users', ['updated_by_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'updated_by_id')
    op.drop_column('products', 'updated_at')
