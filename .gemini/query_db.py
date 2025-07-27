import sys
from app.db.session import SessionLocal
from app.db.models import Tag, User, Store

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_db.py <command>")
        print("Commands: list_tags, list_users, list_stores")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list_tags":
        list_tags()
    elif command == "list_users":
        list_users()
    elif command == "list_stores":
        list_stores()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
