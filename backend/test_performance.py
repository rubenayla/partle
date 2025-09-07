import time
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from app.db.models import Product, User
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Connect to database
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
session = Session()

# Find user
user = session.query(User).filter_by(email="ruben.jimenezmejias@gmail.com").first()
print(f"User ID: {user.id}")

# Test raw SQL query
start = time.time()
result = session.execute(
    text("SELECT COUNT(*) FROM products WHERE creator_id = :user_id"),
    {"user_id": user.id}
).scalar()
print(f"User has {result} products")
print(f"Raw SQL COUNT: {(time.time() - start)*1000:.2f}ms")

# Test raw SQL fetch
start = time.time()
products = session.execute(
    text("SELECT * FROM products WHERE creator_id = :user_id ORDER BY created_at DESC"),
    {"user_id": user.id}
).fetchall()
print(f"Raw SQL fetch {len(products)} products: {(time.time() - start)*1000:.2f}ms")

# Test ORM query
start = time.time()
products = session.query(Product).filter(Product.creator_id == user.id).order_by(Product.created_at.desc()).all()
print(f"ORM fetch {len(products)} products: {(time.time() - start)*1000:.2f}ms")

# Check if index exists
result = session.execute(
    text("SELECT indexname FROM pg_indexes WHERE tablename = 'products' AND indexname LIKE '%creator%'")
).fetchall()
print(f"\nIndexes on creator_id: {result if result else 'None found'}")

session.close()
