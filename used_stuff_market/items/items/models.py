from items.db import Base
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB


class OutboxEntry(Base):
    __tablename__ = "outbox_entries"

    id = Column(Integer(), primary_key=True)
    queue = Column(String(255), nullable=False)
    data = Column(JSONB(), nullable=False)
    retries_left = Column(Integer, nullable=False, default=3)
    when_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
