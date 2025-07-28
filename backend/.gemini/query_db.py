import sys
from app.db.session import SessionLocal
from app.db.models import Tag, User, Store, Product
from datetime import datetime, timedelta

def list_tags():
    db = SessionLocal()
    tags = db.query(Tag).all()
    print("--- Tags ---")
    if not tags:
        print("(No tags found)")
    for tag in tags:
        print(f"ID: {tag.id}, Name: {tag.name}")
    db.close()

def list_users():
    db = SessionLocal()
    users = db.query(User).all()
    print("--- Users ---")
    if not users:
        print(f"(No users found)")
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}")
    db.close()

def list_stores():
    db = SessionLocal()
    stores = db.query(Store).all()
    print("--- Stores ---")
    if not stores:
        print("(No stores found)")
    else:
        print(f"Total stores: {len(stores)}")
        for store in stores:
            print(f"ID: {store.id}, Name: {store.name}, Type: {store.type.value}")
    db.close()

def list_products():
    db = SessionLocal()
    products = db.query(Product).all()
    print("--- Products ---")
    if not products:
        print("(No products found)")
    else:
        print(f"Total products: {len(products)}")
    db.close()

def populate_created_at():
    db = SessionLocal()
    products = db.query(Product).order_by(Product.id.asc()).all()
    updated_count = 0
    
    now = datetime.now()
    two_days_ago = now - timedelta(days=2)
    
    # Distribute dates evenly between two_days_ago and now
    for i, product in enumerate(products):
        time_diff = (now - two_days_ago) / len(products)
        product.created_at = two_days_ago + (time_diff * i)
        updated_count += 1
    
    db.commit()
    print(f"Populated created_at for {updated_count} products with recent distinct values.")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_db.py <command>")
        print("Commands: list_tags, list_users, list_stores, list_products, populate_created_at")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list_tags":
        list_tags()
    elif command == "list_users":
        list_users()
    elif command == "list_stores":
        list_stores()
    elif command == "list_products":
        list_products()
    elif command == "populate_created_at":
        populate_created_at()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
