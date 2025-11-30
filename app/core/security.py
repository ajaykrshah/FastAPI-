from fastapi import Header
from typing import Optional

async def get_correlation_id(x_request_id: Optional[str] = Header(default=None)) -> str:
    return x_request_id or ""
