from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

db_path = Path(__file__).resolve().parents[2] / "partle.db"
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
