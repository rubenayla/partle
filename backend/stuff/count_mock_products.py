
import os
import sys
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.models import Product, Tag

DATABASE_URL = "postgresql://postgres:partl3p4ss@localhost:5432/partle"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def count_mock_products():
    db = SessionLocal()
    try:
        # Find the 'mock-data' tag
        mock_data_tag = db.execute(select(Tag).where(Tag.name == 'mock-data')).scalar_one_or_none()

        if not mock_data_tag:
            print("Tag 'mock-data' not found.")
            return

        # Get all products with the 'mock-data' tag
        products_to_update = db.execute(
            select(Product)
            .join(Product.tags)
            .where(Tag.id == mock_data_tag.id)
        ).scalars().all()

        print(f"Found {len(products_to_update)} products with the 'mock-data' tag.")

    finally:
        db.close()

if __name__ == "__main__":
    count_mock_products()
