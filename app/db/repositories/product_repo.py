from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.product import Product

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> List[Product]:
        res = await self.session.execute(select(Product))
        return list(res.scalars().all())

    async def create(self, name: str, enabled: bool = True, cron: str | None = None, metadata: dict | None = None) -> Product:
        p = Product(name=name, enabled=enabled, cron=cron, metadata=metadata or {})
        self.session.add(p)
        await self.session.flush()
        return p

    async def get(self, id) -> Optional[Product]:
        return await self.session.get(Product, id)

    async def delete(self, id) -> None:
        await self.session.execute(delete(Product).where(Product.id == id))
