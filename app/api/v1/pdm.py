from fastapi import APIRouter, HTTPException, Depends
from ...schemas.pdm import PdmProxyRequest
from ...services.pdm_client import PDMClient
from ...core.security import get_correlation_id

router = APIRouter(tags=["pdm"])
_client = PDMClient()

@router.post("/pdm/call")
async def pdm_call(payload: PdmProxyRequest, correlation_id: str = Depends(get_correlation_id)):
    try:
        resp = await _client.call(payload.service, payload.method, payload.path, query=payload.query, headers=payload.headers, body=payload.body, correlation_id=correlation_id)
        return {"status_code": resp.status_code, "headers": dict(resp.headers), "body": resp.json() if "application/json" in resp.headers.get("content-type","") else resp.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
