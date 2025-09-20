"""merge_heads

Revision ID: bd1cfae45430
Revises: 36b5708b7b23, 7b3c4a2d9f5e
Create Date: 2025-09-20 11:38:04.143358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd1cfae45430'
down_revision: Union[str, Sequence[str], None] = ('36b5708b7b23', '7b3c4a2d9f5e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
