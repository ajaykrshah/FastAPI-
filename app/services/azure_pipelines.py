from typing import Any, Dict
import httpx
from ..core.config import settings

AZ_BASE = f"https://dev.azure.com/{settings.AZDO_ORG}/{settings.AZDO_PROJECT}"

def _auth() -> dict[str,str]:
    # Azure DevOps PAT uses Basic with username empty and PAT as password
    import base64
    token = base64.b64encode(f':{settings.AZDO_PAT}'.encode()).decode()
    return {"Authorization": f"Basic {token}"}

async def trigger_run(pipeline_id: int | None, parameters: dict | None) -> Dict[str, Any]:
    pid = pipeline_id or settings.AZDO_PIPELINE_ID
    url = f"{AZ_BASE}/_apis/pipelines/{pid}/runs?api-version=7.1-preview.1"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, headers=_auth(), json={"resources": {}, "templateParameters": parameters or {}})
        r.raise_for_status()
        d = r.json()
        return {"runId": d.get("id"), "url": d.get("url")}

async def get_status(run_id: str) -> Dict[str, Any]:
    url = f"{AZ_BASE}/_apis/pipelines/{settings.AZDO_PIPELINE_ID}/runs/{run_id}?api-version=7.1-preview.1"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, headers=_auth())
        r.raise_for_status()
        d = r.json()
        return {
            "status": d.get("state"),
            "result": d.get("result"),
            "started": d.get("createdDate"),
            "finished": d.get("finishedDate"),
            "logsUrl": d.get("_links", {}).get("logs", {}).get("href"),
            "timelineUrl": d.get("_links", {}).get("timeline", {}).get("href"),
            "artifacts": d.get("resources", {}).get("repositories", {}),
        }
