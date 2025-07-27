"""Add CHAIN type to StoreType enum

Revision ID: c2dc0d35fa4b
Revises: efc6f531b186
Create Date: 2025-07-27 18:38:25.476800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2dc0d35fa4b'
down_revision: Union[str, Sequence[str], None] = 'efc6f531b186'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE store_type ADD VALUE 'chain'")


def downgrade() -> None:
    op.execute("ALTER TYPE store_type REMOVE VALUE 'chain'")