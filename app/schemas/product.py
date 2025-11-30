from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID

class ProductIn(BaseModel):
    name: str
    enabled: bool = True
    cron: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ProductOut(ProductIn):
    id: UUID
    status: str
    last_updated: str
