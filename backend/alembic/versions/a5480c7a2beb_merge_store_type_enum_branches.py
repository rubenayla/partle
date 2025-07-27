"""merge store type enum branches

Revision ID: a5480c7a2beb
Revises: 6d301db3d9be, 8cdfc51661a9
Create Date: 2025-07-27 19:52:26.146637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5480c7a2beb'
down_revision: Union[str, Sequence[str], None] = ('6d301db3d9be', '8cdfc51661a9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
