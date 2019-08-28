from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from main import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    screen_name = Column(String(140), nullable=False)
    created_at = Column(DateTime, nullable=False)