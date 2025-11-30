from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.execution_history import ExecutionHistory
from ..models.execution_step import ExecutionStep

class ExecutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_history(self, product_id, name: str, metadata: dict | None = None) -> ExecutionHistory:
        h = ExecutionHistory(product_id=product_id, name=name, metadata=metadata or {})
        self.session.add(h)
        await self.session.flush()
        return h

    async def add_step(self, history_id, sequence: int, step_name: str) -> ExecutionStep:
        s = ExecutionStep(history_id=history_id, sequence=sequence, step_name=step_name)
        self.session.add(s)
        await self.session.flush()
        return s

    async def get_history(self, id) -> Optional[ExecutionHistory]:
        return await self.session.get(ExecutionHistory, id)
