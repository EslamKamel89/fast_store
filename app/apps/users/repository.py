from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.apps.users.models import User


class UserRepository():
    def __init__(self , session:AsyncSession):
        self.session = session
        
    async def create(self, name: str, email: str, password_hash: str, role: str = "user")->User:
        user = User(name=name, email=email.lower().strip(), password_hash=password_hash, role=role)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        await self.session.commit()
        return user
    
    async def get_by_email(self , email:str)->Optional[User] :
        stmt = select(User).where(User.email == email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    
    