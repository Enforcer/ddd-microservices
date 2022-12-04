from likes.db import Base
from sqlalchemy import Column, Integer


class Like(Base):
    __tablename__ = "likes"

    item_id = Column(Integer(), primary_key=True)
    liker = Column(Integer(), primary_key=True)
