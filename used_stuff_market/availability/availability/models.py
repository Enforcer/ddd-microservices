from availability.db import Base
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer(), primary_key=True)
    owner_id = Column(UUID(), nullable=False)
    created_at = Column(DateTime(), nullable=False)
    locked_by = Column(UUID(), nullable=True)
    locked_to = Column(DateTime(), nullable=True)
