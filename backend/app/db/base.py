# backend/app/db/base.py
from app.db.base_class import Base
from app.db.models import User, Store, Product, Credential  # models must import Base
from app.db.session import engine


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()

# To start fresh with the right database schema: `poetry run python app/db/base.py`
