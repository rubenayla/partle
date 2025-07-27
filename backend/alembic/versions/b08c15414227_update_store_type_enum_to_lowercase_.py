"""update store type enum to lowercase constants

Revision ID: b08c15414227
Revises: a5480c7a2beb
Create Date: 2025-07-27 19:52:31.236172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b08c15414227'
down_revision: Union[str, Sequence[str], None] = 'a5480c7a2beb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
