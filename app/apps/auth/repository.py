from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.apps.auth.models import RefreshToken
from app.apps.users.models import User
from app.db.models import *
from app.db.repository import BaseRepository


class AuthRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_refresh_token(
        self, user_id: int, expires_in_days: int = 30
    ) -> RefreshToken:
        token_str = RefreshToken.create_token_str()
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
        refresh_token = RefreshToken(token=token_str, user_id=user_id, revoked=False)
        return await self.add(refresh_token, commit=True)

    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def revoke(self, token: str) -> bool:
        r = await self.get_by_token(token)
        if r is None:
            return False
        r.revoked = True
        self.session.add(r)
        await self.session.commit()
        return True

    async def revoke_by_user(self, user_id: int) -> int:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id, RefreshToken.revoked == False
        )
        res = await self.session.execute(stmt)
        rows = res.scalars().all()
        for row in rows:
            row.revoked = True
            self.session.add(row)
        await self.session.commit()
        return len(rows)
