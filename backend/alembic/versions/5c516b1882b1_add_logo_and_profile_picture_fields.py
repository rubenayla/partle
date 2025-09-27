"""Add logo and profile picture fields

Revision ID: 5c516b1882b1
Revises: ffbebe72d891
Create Date: 2025-09-27 22:04:50.740486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c516b1882b1'
down_revision: Union[str, Sequence[str], None] = 'ffbebe72d891'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add logo fields to stores table
    op.add_column('stores', sa.Column('logo_data', sa.LargeBinary(), nullable=True))
    op.add_column('stores', sa.Column('logo_filename', sa.String(), nullable=True))
    op.add_column('stores', sa.Column('logo_content_type', sa.String(), nullable=True))

    # Add profile picture fields to users table
    op.add_column('users', sa.Column('profile_picture_data', sa.LargeBinary(), nullable=True))
    op.add_column('users', sa.Column('profile_picture_filename', sa.String(), nullable=True))
    op.add_column('users', sa.Column('profile_picture_content_type', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove profile picture fields from users table
    op.drop_column('users', 'profile_picture_content_type')
    op.drop_column('users', 'profile_picture_filename')
    op.drop_column('users', 'profile_picture_data')

    # Remove logo fields from stores table
    op.drop_column('stores', 'logo_content_type')
    op.drop_column('stores', 'logo_filename')
    op.drop_column('stores', 'logo_data')
