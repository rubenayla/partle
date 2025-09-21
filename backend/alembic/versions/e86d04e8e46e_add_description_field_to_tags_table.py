"""Add description field to tags table

Revision ID: e86d04e8e46e
Revises: af9392ae8fa0
Create Date: 2025-09-21 18:29:36.031495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e86d04e8e46e'
down_revision: Union[str, Sequence[str], None] = 'af9392ae8fa0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tags', sa.Column('description', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('tags', 'description')
