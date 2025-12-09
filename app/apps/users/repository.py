from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.apps.users.models import User
from app.db.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def create(
        self, name: str, email: str, password_hash: str, role: str = "user"
    ) -> User:
        user = User(
            name=name,
            email=email.lower().strip(),
            password_hash=password_hash,
            role=role,
        )
        return await self.add(user, commit=True)

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
