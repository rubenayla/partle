import sys
from app.db.session import SessionLocal
from app.db.models import Tag, User, Store, Product
from datetime import datetime, timedelta
from sqlalchemy import or_, func

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
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}, Store ID: {product.store_id}, Creator ID: {product.creator_id}")
    db.close()

def search_products(query_str: str):
    db = SessionLocal()
    search_term = f"%{query_str}%"
    products = db.query(Product).filter(Product.name.ilike(search_term)).all()
    print(f"--- Products matching '{query_str}' ---")
    if not products:
        print("(No products found matching query)")
    else:
        print(f"Total products matching: {len(products)}")
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}, Store ID: {product.store_id}, Creator ID: {product.creator_id}")
    db.close()

def query_products_with_full_filters(
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    tags: str | None = None,
    sort_by: str | None = None,
    limit: int = 20,
    offset: int = 0,
):
    db = SessionLocal()
    query = db.query(Product)

    if q:
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        if tag_list:
            query = query.join(Product.tags).filter(Tag.name.in_(tag_list))

    if sort_by == "created_at":
        query = query.order_by(Product.created_at.desc())
    elif sort_by == "created_at_asc":
        query = query.order_by(Product.created_at.asc())
    elif sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "random":
        query = query.order_by(func.random())

    products = query.offset(offset).limit(limit).all()

    print(f"--- Products with full filters (q='{q}', min_price={min_price}, max_price={max_price}, sort_by='{sort_by}', limit={limit}, offset={offset}) ---")
    if not products:
        print("(No products found with these filters)")
    else:
        print(f"Total products found: {len(products)}")
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}, Store ID: {product.store_id}, Creator ID: {product.creator_id}")
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
    elif command == "search_products":
        if len(sys.argv) < 3:
            print("Usage: python query_db.py search_products <query_string>")
            sys.exit(1)
        search_products(sys.argv[2])
    elif command == "query_products_with_full_filters":
        # Example usage: poetry run python .gemini/query_db.py query_products_with_full_filters --q test2 --sort_by relevance
        # Parse arguments manually for simplicity
        args = sys.argv[2:]
        params = {}
        i = 0
        while i < len(args):
            if args[i].startswith("--"):
                key = args[i][2:]
                if i + 1 < len(args) and not args[i+1].startswith("--"):
                    value = args[i+1]
                    params[key] = value
                    i += 2
                else:
                    params[key] = True # For boolean flags if any
                    i += 1
            else:
                i += 1 # Skip unexpected args
        
        query_products_with_full_filters(
            q=params.get("q"),
            min_price=float(params["min_price"]) if "min_price" in params else None,
            max_price=float(params["max_price"]) if "max_price" in params else None,
            tags=params.get("tags"),
            sort_by=params.get("sort_by"),
            limit=int(params.get("limit", 20)),
            offset=int(params.get("offset", 0)),
        )
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
