# backend/app/db/models.py
from typing import Optional, TYPE_CHECKING
from enum import Enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Enum as PgEnum,
    Numeric,
    Text,
    LargeBinary,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base


class StoreType(str, Enum):
    PHYSICAL = "physical"
    ONLINE = "online"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    stores: Mapped[list["Store"]] = relationship(back_populates="owner")
    credentials: Mapped[list["Credential"]] = relationship(back_populates="user")
    products: Mapped[list["Product"]] = relationship(
        back_populates="creator", foreign_keys="Product.creator_id"
    )
    updated_products: Mapped[list["Product"]] = relationship(
        back_populates="updated_by", foreign_keys="Product.updated_by_id"
    )


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[StoreType] = mapped_column(
        PgEnum(StoreType, name="store_type"), default=StoreType.PHYSICAL
    )
    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lon: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    homepage: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    owner_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    owner: Mapped[Optional[User]] = relationship(back_populates="stores")
    products: Mapped[list["Product"]] = relationship(back_populates="store")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    spec: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lon: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    store_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stores.id", ondelete="SET NULL"), nullable=True
    )
    store: Mapped[Optional[Store]] = relationship(back_populates="products")
    creator_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    creator: Mapped[Optional[User]] = relationship(
        back_populates="products", foreign_keys=[creator_id]
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    updated_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    updated_by: Mapped[Optional[User]] = relationship(
        back_populates="updated_products", foreign_keys=[updated_by_id]
    )


class Credential(Base):
    __tablename__ = "credentials"

    id: Mapped[int] = mapped_column(primary_key=True)
    credential_id: Mapped[bytes] = mapped_column(LargeBinary, unique=True)
    public_key: Mapped[bytes] = mapped_column(LargeBinary)
    sign_count: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="credentials")
