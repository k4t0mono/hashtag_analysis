from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from main import Base


class Hashtag(Base):
    __tablename__ = 'hashtag'

    name = Column(String(150), nullable=False)