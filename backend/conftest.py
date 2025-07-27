import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.v1 import parts, stores, auth, tags, products, external
from app.auth import security
from app.db.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db")
def db_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Dependency override for tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[parts.get_db] = override_get_db
app.dependency_overrides[stores.get_db] = override_get_db
app.dependency_overrides[auth.get_db] = override_get_db
app.dependency_overrides[tags.get_db] = override_get_db
app.dependency_overrides[security.get_db] = override_get_db
app.dependency_overrides[products.get_db] = override_get_db
app.dependency_overrides[external.get_db] = override_get_db

@pytest.fixture(name="client")
def client_fixture():
    return TestClient(app)
