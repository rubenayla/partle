from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    parts = relationship("Part", back_populates="store")


class Part(Base):
    __tablename__ = "parts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sku = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    price = Column(Float, nullable=True)

    store_id = Column(Integer, ForeignKey("stores.id"))
    store = relationship("Store", back_populates="parts")
