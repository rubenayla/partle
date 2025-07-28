import sys
from app.db.session import SessionLocal
from app.db.models import Tag, User, Store, Product

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
        print("(No users found)")
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

def list_products(store_id: int = None):
    db = SessionLocal()
    query = db.query(Product)
    if store_id:
        query = query.filter(Product.store_id == store_id)
    products = query.all()
    print("--- Products ---")
    if not products:
        print("(No products found)")
    else:
        print(f"Total products: {len(products)}")
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}, Store ID: {product.store_id}, Image URL: {product.image_url}")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_db.py <command> [args]")
        print("Commands: list_tags, list_users, list_stores, list_products [store_id]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list_tags":
        list_tags()
    elif command == "list_users":
        list_users()
    elif command == "list_stores":
        list_stores()
    elif command == "list_products":
        store_id = int(sys.argv[2]) if len(sys.argv) > 2 else None
        list_products(store_id)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)