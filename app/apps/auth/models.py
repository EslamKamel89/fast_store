from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlmodel import (
    Boolean,
    Column,
    DateTime,
    Field,
    Relationship,
    SQLModel,
    String,
    text,
)

if TYPE_CHECKING:
    from apps.users.models import User


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"  # type: ignore
    id: Optional[int] = Field(primary_key=True, default=None)
    token: str = Field(
        sa_column=Column(String(255), nullable=False, unique=True, index=True)
    )
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    user: Optional["User"] = Relationship(back_populates="refresh_tokens")
    revoked: bool = Field(
        default=False, sa_column=Column(Boolean, nullable=False, default=False)
    )
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30),
        sa_column=Column(DateTime(timezone=True), nullable=False),
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

    @classmethod
    def create_token_str(cls) -> str:
        return uuid4().hex
