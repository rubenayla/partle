"""add_created_at_to_product

Revision ID: ad27e536d3af
Revises: b08c15414227
Create Date: 2025-07-28 23:26:45.172304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad27e536d3af'
down_revision: Union[str, Sequence[str], None] = 'b08c15414227'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))


def downgrade() -> None:
    op.drop_column('products', 'created_at')
