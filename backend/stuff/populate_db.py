
import asyncio
from sqlalchemy.future import select
import httpx
from app.db.session import SessionLocal
from app.db.models import Product, Tag

def populate_db():
    """Populate the database with mock data."""
    with httpx.Client() as client:
        response = client.get("https://dummyjson.com/products")
        data = response.json()
        products = data["products"]

    session = SessionLocal()
    try:
        tag = session.execute(select(Tag).filter_by(name="mock-data")).scalar_one_or_none()
        if not tag:
            tag = Tag(name="mock-data")
            session.add(tag)
            session.commit()
            session.refresh(tag)

        for product_data in products:
            product = Product(
                name=product_data["title"],
                description=product_data["description"],
                price=product_data["price"],
                tags=[tag]
            )
            session.add(product)

        session.commit()
    finally:
        session.close()

def main():
    """Script entrypoint."""
    populate_db()

if __name__ == "__main__":
    main()
