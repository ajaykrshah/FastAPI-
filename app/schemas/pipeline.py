from pydantic import BaseModel
from typing import Any, Dict, Optional

class PipelineRunRequest(BaseModel):
    pipelineId: Optional[int] = None
    parameters: Optional[Dict[str, Any]] = None

class PipelineRunResponse(BaseModel):
    runId: str
    url: str
