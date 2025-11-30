from fastapi import APIRouter
from .v1.scripts import router as scripts_router
from .v1.pdm import router as pdm_router
from .v1.pipelines import router as pipelines_router
from .v1.products import router as products_router
from .v1.dashboard import router as dashboard_router

api_router = APIRouter()
api_router.include_router(scripts_router)
api_router.include_router(pdm_router)
api_router.include_router(pipelines_router)
api_router.include_router(products_router)
api_router.include_router(dashboard_router)
