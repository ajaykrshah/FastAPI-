from fastapi import APIRouter
router = APIRouter(tags=["dashboard"])

@router.get("/dashboard")
async def dashboard():
    # Placeholder; implement queries to compute KPIs from execution_history/step semantics.
    return {"totals": {"products": 0, "enabled": 0}, "notifications": {"total":0,"last24h":0}, "patches": {"created":0,"failed":0,"published":0}, "trend": [], "recentFailures": [], "lastRun": None}
