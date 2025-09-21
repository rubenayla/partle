"""Add SKU field with per-store uniqueness

Revision ID: ffbebe72d891
Revises: e86d04e8e46e
Create Date: 2025-09-21 18:44:48.519870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffbebe72d891'
down_revision: Union[str, Sequence[str], None] = 'e86d04e8e46e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add SKU column
    op.add_column('products', sa.Column('sku', sa.String(50), nullable=True))

    # Create index on SKU for faster lookups
    op.create_index('ix_products_sku', 'products', ['sku'])

    # Add unique constraint on store_id and sku
    op.create_unique_constraint('unique_store_sku', 'products', ['store_id', 'sku'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop unique constraint
    op.drop_constraint('unique_store_sku', 'products', type_='unique')

    # Drop index
    op.drop_index('ix_products_sku', 'products')

    # Drop column
    op.drop_column('products', 'sku')
