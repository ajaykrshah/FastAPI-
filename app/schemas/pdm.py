from pydantic import BaseModel
from typing import Any, Dict, Optional

class PdmProxyRequest(BaseModel):
    service: str
    method: str
    path: str
    query: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[Any] = None
