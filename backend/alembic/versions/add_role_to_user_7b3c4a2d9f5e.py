"""Add role to user

Revision ID: 7b3c4a2d9f5e
Revises: f20a588a77a0
Create Date: 2025-09-18 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7b3c4a2d9f5e'
down_revision = 'f20a588a77a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the user_role enum type
    user_role = postgresql.ENUM('user', 'admin', 'moderator', name='user_role')
    user_role.create(op.get_bind())

    # Add role column to users table with default value 'user'
    op.add_column('users', sa.Column('role', user_role, nullable=False, server_default='user'))


def downgrade() -> None:
    # Remove the role column
    op.drop_column('users', 'role')

    # Drop the enum type
    op.execute('DROP TYPE IF EXISTS user_role')