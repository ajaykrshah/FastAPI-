from sqlalchemy import Column, String, ForeignKey, Text, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import sqlalchemy as sa
import uuid
from ..base import Base

run_status = sa.Enum('Pending','Running','Failed','Completed', name='run_status')

class ExecutionHistory(Base):
    __tablename__ = "execution_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    status = Column(run_status, nullable=False, server_default='Pending')
    pipeline_run_id = Column(Text, nullable=True)
    duration_ms = Column(BigInteger, nullable=True)
    metadata = Column(JSONB, nullable=False, server_default=sa.text("'{}'::jsonb"))
