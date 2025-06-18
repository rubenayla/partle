# backend/app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    address = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    spec = Column(String)
    price = Column(Float)
    url = Column(String)
    store_id = Column(Integer, ForeignKey("stores.id"))
    store = relationship("Store")
