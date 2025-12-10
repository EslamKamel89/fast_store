from decimal import Decimal
from typing import Any, Optional, Sequence
from unicodedata import decimal

from apps.catalog.models import Product
from db.repository import BaseRepository, UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        self.session = session
        return super().__init__(session, Product)

    async def get_by_id(
        self, product_id: int, *, with_relationships: bool = True
    ) -> Optional[Product]:
        if with_relationships:
            stmt = (
                select(Product)
                .where(Product.id == product_id)
                .options(selectinload(Product.categories))  # type: ignore
            )
            res = await self.session.execute(stmt)
            return res.scalar_one_or_none()
        return await self.get(product_id)

    async def get_by_slug(
        self, slug: str, *, with_relationships: bool = True
    ) -> Optional[Product]:
        if with_relationships:
            stmt = (select(Product).where(Product.slug == slug)).options(
                selectinload(Product.categories)  # type: ignore
            )
            res = await self.session.execute(stmt)
            return res.scalar_one_or_none()
        return await self.get_by_slug(slug)

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        query: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
    ) -> Sequence[Product]: ...

    async def count(
        self,
        *,
        query: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        category_id: Optional[int] = None,
    ) -> int: ...

    async def create(self, *, data: dict[str, Any], commit: bool = True): ...

    async def update(
        self, product: Product, *, fields: dict[str, Any], commit: bool = True
    ) -> Product: ...

    async def delete(self, product: Product, *, commit: bool = True) -> None: ...

    async def reverse_stock(
        self, product_id: int, quantity: int, *, uow: Optional[UnitOfWork] = None
    ) -> bool: ...
