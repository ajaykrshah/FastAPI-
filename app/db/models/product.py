from sqlalchemy import Column, String, Boolean, Text, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import sqlalchemy as sa
import uuid
from ..base import Base

run_status = sa.Enum('Pending','Running','Failed','Completed', name='run_status')

class Product(Base):
    __tablename__ = "product"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    enabled = Column(Boolean, nullable=False, server_default=sa.sql.expression.true())
    cron = Column(Text, nullable=True)
    status = Column(run_status, nullable=False, server_default='Pending')
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    metadata = Column(JSONB, nullable=False, server_default=sa.text("'{}'::jsonb"))
