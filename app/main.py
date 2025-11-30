from fastapi import FastAPI
from .core.config import settings
from .core.logging import CorrelationIdMiddleware
from .api.router import api_router

app = FastAPI(title="PDM/Azure/GitHub Service")

@app.get("/health")
async def health(): return {"ok": True}
@app.get("/ready")
async def ready(): return {"ready": True}

app.add_middleware(CorrelationIdMiddleware)
app.include_router(api_router, prefix=settings.API_PREFIX)
