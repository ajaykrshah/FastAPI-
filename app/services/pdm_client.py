from typing import Dict, Any
import httpx
from base64 import b64encode
from ..core.config import settings

class PDMClient:
    def __init__(self) -> None:
        self.services = {s["name"]: s["baseUrl"] for s in settings.PDM_SERVICES_JSON}
        cred = f"{settings.PDM_USER}:{settings.PDM_PASS}".encode()
        self.auth_header = {"Authorization": "Basic " + b64encode(cred).decode()}

    async def call(self, service: str, method: str, path: str, query: Dict[str, Any] | None=None, headers: Dict[str,str] | None=None, body: Any | None=None, correlation_id: str | None=None) -> httpx.Response:
        base = self.services.get(service)
        if not base or not base.lower().startswith("https://"):
            raise ValueError("Unknown service or non-HTTPS baseUrl")
        url = base.rstrip("/") + "/" + path.lstrip("/")
        req_headers = {"Accept": "application/json", **self.auth_header}
        if headers:
            req_headers.update({k:v for k,v in headers.items() if k.lower() != "authorization"})
        if correlation_id:
            req_headers["X-Request-ID"] = correlation_id
        timeout = httpx.Timeout(20.0, connect=10.0)
        limits = httpx.Limits(max_keepalive_connections=10, max_connections=50)
        async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
            resp = await client.request(method.upper(), url, params=query, headers=req_headers, json=body)
            return resp
