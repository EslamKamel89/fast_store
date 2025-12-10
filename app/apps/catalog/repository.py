from decimal import Decimal
from typing import Any, Optional, Sequence
from unicodedata import decimal

from db.repository import BaseRepository, UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import catalog_models as catalog


class ProductRepository(BaseRepository[catalog.Product]):
    def __init__(self, session: AsyncSession):
        return super().__init__(session, catalog.Product)

    async def get_by_id(
        self, product_id: int, *, with_relationships: bool = True
    ) -> Optional[catalog.Product]: ...

    async def get_by_slug(
        self, slug: str, *, with_relationships: bool = True
    ) -> Optional[catalog.Product]: ...

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        query: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
    ) -> Sequence[catalog.Product]: ...

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
        self, product: catalog.Product, *, fields: dict[str, Any], commit: bool = True
    ) -> catalog.Product: ...

    async def delete(
        self, product: catalog.Product, *, commit: bool = True
    ) -> None: ...

    async def reverse_stock(
        self, product_id: int, quantity: int, *, uow: Optional[UnitOfWork] = None
    ) -> bool: ...
