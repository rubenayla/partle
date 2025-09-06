"""Add currency field to products

Revision ID: f20a588a77a0
Revises: 6c21a37be6b8
Create Date: 2025-09-06 18:13:20.412941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f20a588a77a0'
down_revision: Union[str, Sequence[str], None] = '6c21a37be6b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('currency', sa.String(length=10), nullable=True, server_default='€'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'currency')
