"""Add image storage fields to products

Revision ID: 6c21a37be6b8
Revises: ad27e536d3af
Create Date: 2025-08-31 18:11:58.049340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c21a37be6b8'
down_revision: Union[str, Sequence[str], None] = 'ad27e536d3af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add image storage fields to products table
    op.add_column('products', sa.Column('image_data', sa.LargeBinary(), nullable=True))
    op.add_column('products', sa.Column('image_filename', sa.String(), nullable=True))
    op.add_column('products', sa.Column('image_content_type', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove image storage fields from products table
    op.drop_column('products', 'image_content_type')
    op.drop_column('products', 'image_filename')
    op.drop_column('products', 'image_data')
