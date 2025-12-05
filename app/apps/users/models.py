from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, String, text

if TYPE_CHECKING:
    from apps.auth.models import RefreshToken


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        sa_column=Column(String(200), nullable=False, index=True, unique=True)
    )
    name: str = Field(sa_column=Column(String(100), nullable=False))
    password_hash: str = Field(sa_column=Column(String(255), nullable=False))
    role: str = Field(sa_column=Column(String(50)), default="user")
    refresh_tokens: list["RefreshToken"] = Relationship(back_populates="user")
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
