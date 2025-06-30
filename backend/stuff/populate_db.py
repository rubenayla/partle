
import asyncio
import httpx
from sqlalchemy.future import select
from app.db.session import get_session
from app.db.models import Product, Tag

async def populate_db():
    """Populate the database with mock data."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/products")
        data = response.json()
        products = data["products"]

    async with get_session() as session:
        tag = await session.execute(select(Tag).filter_by(name="mock-data"))
        tag = tag.scalar_one_or_none()
        if not tag:
            tag = Tag(name="mock-data")
            session.add(tag)
            await session.commit()
            await session.refresh(tag)

        for product_data in products:
            product = Product(
                name=product_data["title"],
                description=product_data["description"],
                price=product_data["price"],
                tags=[tag]
            )
            session.add(product)

        await session.commit()

def main():
    """Script entrypoint."""
    asyncio.run(populate_db())

if __name__ == "__main__":
    main()
