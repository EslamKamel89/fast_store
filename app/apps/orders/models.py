from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, text
from sqlmodel import Column, DateTime, Field, Integer, Relationship, SQLModel

if TYPE_CHECKING:
    from app.apps.catalog.models import Product
    from app.apps.users.models import User


class Order(SQLModel, table=True):
    __tablename__ = "orders"  # type: ignore
    id: Optional[int] = Field(primary_key=True, default=None)
    user_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
        ),
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
    user: Optional["User"] = Relationship(back_populates="orders")
    items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"  # type: ignore
    id: Optional[int] = Field(primary_key=True, default=None)
    order_id: Optional[int] = Field(
        sa_column=Column(
            ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
        )
    )
    product_id: Optional[int] = Field(
        sa_column=Column(
            ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True
        )
    )
    quantity: int = Field(sa_column=Column(Integer(), nullable=False))
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
    order: "Order" = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="order_items")
