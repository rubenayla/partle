# backend/app/models.py
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .models import Store

from enum import Enum
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey,
    Enum as PgEnum, Numeric, Text
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base


class StoreType(str, Enum):
    PHYSICAL = "physical"
    ONLINE   = "online"


class User(Base):
    __tablename__ = "users"

    id:          Mapped[int] = mapped_column(primary_key=True)
    email:       Mapped[str] = mapped_column(String, unique=True, index=True,
                                             comment="Login / contact e-mail")
    password_hash: Mapped[str] = mapped_column(String, comment="Argon2 hash")

    # -- reverse access: user.stores --
    stores: Mapped[list["Store"]] = relationship(back_populates="owner")


class Store(Base):
    __tablename__ = "stores"

    id:        Mapped[int] = mapped_column(primary_key=True)
    name:      Mapped[str] = mapped_column(String, comment="Public display name")
    type:      Mapped[StoreType] = mapped_column(
        PgEnum(StoreType, name="store_type"), default=StoreType.PHYSICAL,
        comment="physical = has premises; online = pure e-commerce"
    )

    # location (optional)
    lat:       Mapped[float | None] = mapped_column(Float, nullable=True,
                        comment="Latitude WGS84 (nullable for online stores)")
    lon:       Mapped[float | None] = mapped_column(Float, nullable=True,
                        comment="Longitude WGS84")
    address:   Mapped[str | None]  = mapped_column(String, nullable=True)
    homepage:  Mapped[str | None]  = mapped_column(String, nullable=True)

    # ownership
    owner_id:  Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    owner: Mapped[User | None] = relationship(back_populates="stores")

    # reverse access: store.products
    products: Mapped[list["Product"]] = relationship(back_populates="store")


class Product(Base):
    __tablename__ = "products"

    id:        Mapped[int] = mapped_column(primary_key=True)
    name:      Mapped[str] = mapped_column(String, comment="Canonical product name")
    spec:      Mapped[str | None] = mapped_column(String, nullable=True,
                        comment="Short spec/variant (e.g. `6-pin JST`)")
    price:     Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    url:       Mapped[str | None] = mapped_column(String, nullable=True,
                        comment="Original listing URL if scraped (Amazon etc.)")

    # optional item-level position
    lat:       Mapped[float | None] = mapped_column(Float, nullable=True)
    lon:       Mapped[float | None] = mapped_column(Float, nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # store relation (nullable → unknown vendor allowed)
    store_id:  Mapped[int | None] = mapped_column(
        ForeignKey("stores.id", ondelete="SET NULL"), nullable=True
    )
    store: Mapped[Optional["Store"]] = relationship(back_populates="products")
