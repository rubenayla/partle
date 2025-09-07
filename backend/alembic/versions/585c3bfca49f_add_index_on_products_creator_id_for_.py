"""Add index on products.creator_id for performance

Revision ID: 585c3bfca49f
Revises: 2ac373f73968
Create Date: 2025-09-07 12:41:39.470121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '585c3bfca49f'
down_revision: Union[str, Sequence[str], None] = '2ac373f73968'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create index on creator_id for better performance on "My Products" queries
    op.create_index('ix_products_creator_id', 'products', ['creator_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the index
    op.drop_index('ix_products_creator_id', 'products')
