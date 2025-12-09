from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):

    def __init__(self, session: AsyncSession, model: Type[ModelT]):
        self.session = session
        self.model = model

    async def get(self, id: Any) -> Optional[ModelT]:
        return await self.session.get(self.model, id)

    async def list(
        self, *, offset: int | None = None, limit: int | None = None
    ) -> Sequence[ModelT]:
        stmt = select(self.model)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def add(
        self, instance: ModelT, *, commit: bool = False, refresh: bool = True
    ) -> ModelT:
        self.session.add(instance)
        await self.session.flush()
        if commit:
            await self.session.commit()
        if refresh:
            await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelT, *, commit: bool = False) -> None:
        await self.session.delete(instance)
        if commit:
            await self.session.commit()


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def flush(self) -> None:
        await self.session.flush()
