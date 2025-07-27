"""Recreate store_type enum with chain

Revision ID: 6d301db3d9be
Revises: c2dc0d35fa4b
Create Date: 2025-07-27 18:51:22.972010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d301db3d9be'
down_revision: Union[str, Sequence[str], None] = 'c2dc0d35fa4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE store_type RENAME TO store_type_old")
    op.execute("CREATE TYPE store_type AS ENUM ('physical', 'online', 'chain')")
    op.execute("ALTER TABLE stores ALTER COLUMN type TYPE store_type USING type::text::store_type")


def downgrade() -> None:
    op.execute("ALTER TABLE stores ALTER COLUMN type TYPE store_type_old USING type::text::store_type_old")
    op.execute("DROP TYPE store_type")
    op.execute("ALTER TYPE store_type_old RENAME TO store_type")