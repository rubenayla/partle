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
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
        batch_op.add_column(sa.Column('updated_by_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_products_updated_by_id_users', 'users', ['updated_by_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('fk_products_updated_by_id_users', type_='foreignkey')
        batch_op.drop_column('updated_by_id')
        batch_op.drop_column('updated_at')
