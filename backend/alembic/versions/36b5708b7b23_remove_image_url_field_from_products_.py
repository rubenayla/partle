"""Remove image_url field from products table

Revision ID: 36b5708b7b23
Revises: 585c3bfca49f
Create Date: 2025-09-07 13:14:08.005097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36b5708b7b23'
down_revision: Union[str, Sequence[str], None] = '585c3bfca49f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the image_url column from products table
    op.drop_column('products', 'image_url')


def downgrade() -> None:
    """Downgrade schema."""
    # Re-add the image_url column
    op.add_column('products', sa.Column('image_url', sa.String(), nullable=True))
