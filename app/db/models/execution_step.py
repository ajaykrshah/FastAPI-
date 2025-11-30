from sqlalchemy import Column, String, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
import sqlalchemy as sa
import uuid
from ..base import Base

run_status = sa.Enum('Pending','Running','Failed','Completed', name='run_status')

class ExecutionStep(Base):
    __tablename__ = "execution_step"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    history_id = Column(UUID(as_uuid=True), ForeignKey("execution_history.id", ondelete="CASCADE"), nullable=False)
    sequence = Column(Integer, nullable=False)
    step_name = Column(String, nullable=False)
    scripting = Column(JSONB, nullable=False, server_default=sa.text("'{}'::jsonb"))
    script_output = Column(JSONB, nullable=False, server_default=sa.text("'{}'::jsonb"))
    status = Column(run_status, nullable=False, server_default='Pending')
    started_at = Column(sa.TIMESTAMP(timezone=True), nullable=True)
    finished_at = Column(sa.TIMESTAMP(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)

    __table_args__ = (sa.UniqueConstraint("history_id", "sequence"),)
