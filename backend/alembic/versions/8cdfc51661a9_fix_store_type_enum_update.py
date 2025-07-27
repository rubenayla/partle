"""fix_store_type_enum_update

Revision ID: 8cdfc51661a9
Revises: 6d301db3d9be
Create Date: 2025-07-27 18:59:40.731366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cdfc51661a9'
down_revision: Union[str, Sequence[str], None] = 'c2dc0d35fa4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Rename the existing enum type to avoid conflicts
    op.execute("ALTER TYPE store_type RENAME TO store_type_old")
    
    # Step 2: Create the new enum type with all required values
    op.execute("CREATE TYPE store_type AS ENUM ('physical', 'online', 'chain')")
    
    # Step 3: Change the column type to TEXT temporarily
    op.execute("ALTER TABLE stores ALTER COLUMN type TYPE TEXT")
    
    # Step 4: Normalize any uppercase values to lowercase
    op.execute("UPDATE stores SET type = LOWER(type)")
    
    # Step 5: Update the column to use the new enum type
    op.execute("ALTER TABLE stores ALTER COLUMN type TYPE store_type USING type::store_type")
    
    # Step 6: Clean up the old enum type
    op.execute("DROP TYPE store_type_old")


def downgrade() -> None:
    """Downgrade schema."""
    # Step 1: Rename current enum to old
    op.execute("ALTER TYPE store_type RENAME TO store_type_new")
    
    # Step 2: Recreate the old enum without 'chain'
    op.execute("CREATE TYPE store_type AS ENUM ('physical', 'online')")
    
    # Step 3: Change column to TEXT temporarily  
    op.execute("ALTER TABLE stores ALTER COLUMN type TYPE TEXT")
    
    # Step 4: Update column to use old enum (this will fail if 'chain' values exist)
    op.execute("ALTER TABLE stores ALTER COLUMN type TYPE store_type USING type::store_type")
    
    # Step 5: Clean up
    op.execute("DROP TYPE store_type_new")
