from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ...api.deps import get_db
from ...db.repositories.product_repo import ProductRepository
from ...schemas.product import ProductIn, ProductOut

router = APIRouter(tags=["products"])

@router.get("/products")
async def list_products(db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    items = await repo.list()
    return [{"id": p.id, "name": p.name, "enabled": p.enabled, "cron": p.cron, "status": p.status, "last_updated": p.last_updated.isoformat(), "metadata": p.metadata} for p in items]

@router.post("/products")
async def create_product(payload: ProductIn, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    p = await repo.create(payload.name, payload.enabled, payload.cron, payload.metadata)
    await db.commit()
    return {"id": p.id, "name": p.name, "enabled": p.enabled, "cron": p.cron, "status": p.status, "last_updated": p.last_updated.isoformat(), "metadata": p.metadata}
