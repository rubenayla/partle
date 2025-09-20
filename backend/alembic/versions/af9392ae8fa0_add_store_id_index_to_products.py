"""add_store_id_index_to_products

Revision ID: af9392ae8fa0
Revises: bd1cfae45430
Create Date: 2025-09-20 11:38:11.442196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af9392ae8fa0'
down_revision: Union[str, Sequence[str], None] = 'bd1cfae45430'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create index on store_id for faster store product queries
    op.create_index('ix_products_store_id', 'products', ['store_id'])

    # Also add composite index for common query patterns
    op.create_index('ix_products_store_id_created_at', 'products', ['store_id', 'created_at'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_products_store_id_created_at', table_name='products')
    op.drop_index('ix_products_store_id', table_name='products')
