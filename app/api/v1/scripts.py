from fastapi import APIRouter, Query
from typing import Optional, List
from ...services.github_scripts import list_python_scripts
from ...core.config import settings
from ...schemas.scripts import ScriptInfo

router = APIRouter(tags=["scripts"])

@router.get("/scripts", response_model=List[ScriptInfo])
async def get_scripts(prefix: Optional[str] = Query(default=None), pattern: Optional[str] = Query(default=None), page: int = 1, pageSize: int = 100):
    items = await list_python_scripts(settings.GITHUB_ORG, settings.GITHUB_REPO, settings.GITHUB_BRANCH, prefix, pattern)
    # simple pagination
    start = (page-1)*pageSize
    end = start + pageSize
    return [ScriptInfo(**i) for i in items[start:end]]
