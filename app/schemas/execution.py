from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from uuid import UUID

class ExecutionStepOut(BaseModel):
    sequence: int
    step_name: str
    scripting: Dict[str, Any]
    script_output: Dict[str, Any]
    status: str

class ExecutionHistoryOut(BaseModel):
    id: UUID
    product_id: UUID
    name: str
    status: str
    steps: List[ExecutionStepOut] = []
