from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlmodel import (
    Column,
    DateTime,
    Field,
    ForeignKey,
    Numeric,
    Relationship,
    SQLModel,
    String,
    text,
)

if TYPE_CHECKING:
    from app.apps.orders.models import OrderItem


class ProductCategory(SQLModel, table=True):
    __tablename__ = "product_categories"  # type: ignore
    product_id: int = Field(
        sa_column=Column(
            ForeignKey("products.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        ),
    )
    category_id: int = Field(
        sa_column=Column(
            ForeignKey("categories.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )


class Category(SQLModel, table=True):
    __tablename__ = "categories"  # type: ignore
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(
        sa_column=Column(String(100), nullable=False, unique=True, index=True)
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP"),
        ),
    )
    products: list["Product"] = Relationship(
        back_populates="categories", link_model=ProductCategory
    )


class Product(SQLModel, table=True):
    __tablename__ = "products"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(
        sa_column=Column(String(100), unique=True, index=True, nullable=False)
    )
    price: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP"),
        ),
    )
    categories: list["Category"] = Relationship(
        back_populates="products", link_model=ProductCategory
    )
    order_items: list["OrderItem"] = Relationship(
        back_populates="product",
    )
