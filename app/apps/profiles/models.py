from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Nullable, UniqueConstraint
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, String, text

# if TYPE_CHECKING:
from app.apps.users.models import User


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"  # type: ignore
    __table_args__ = (UniqueConstraint("user_id", name="uq_profiles_user_id"),)
    id: Optional[int] = Field(primary_key=True, nullable=True)
    user_id: Optional[int] = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
        )
    )
    bio: Optional[str] = Field(
        default=None, sa_column=Column(String(500), nullable=True)
    )
    avatar_url: Optional[str] = Field(
        default=None, sa_column=Column(String(500), nullable=True)
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
    user: "User" = Relationship(back_populates="profile")
