"""add_product_reviews_table

Revision ID: d7d41e601bcb
Revises: 5c516b1882b1
Create Date: 2025-11-04 20:11:19.881750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7d41e601bcb'
down_revision: Union[str, Sequence[str], None] = '5c516b1882b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'product_reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('product_rating', sa.Integer(), nullable=False),
        sa.Column('info_rating', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('helpful_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('product_id', 'user_id', name='unique_product_user_review')
    )
    op.create_index('ix_product_reviews_product_id', 'product_reviews', ['product_id'])
    op.create_index('ix_product_reviews_user_id', 'product_reviews', ['user_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_product_reviews_user_id', table_name='product_reviews')
    op.drop_index('ix_product_reviews_product_id', table_name='product_reviews')
    op.drop_table('product_reviews')
