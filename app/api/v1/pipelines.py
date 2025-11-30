from fastapi import APIRouter, HTTPException
from ...services.azure_pipelines import trigger_run, get_status
from ...schemas.pipeline import PipelineRunRequest, PipelineRunResponse

router = APIRouter(tags=["pipelines"])

@router.post("/pipelines/run", response_model=PipelineRunResponse)
async def run_pipeline(body: PipelineRunRequest):
    data = await trigger_run(body.pipelineId, body.parameters)
    return PipelineRunResponse(**data)

@router.get("/pipelines/status/{run_id}")
async def pipeline_status(run_id: str):
    return await get_status(run_id)
