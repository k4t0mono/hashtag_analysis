from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from get_tweets import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String(128), primary_key=True)
    screen_name = Column(String(140), nullable=False)
    created_at = Column(DateTime, nullable=False)

    auto_score = Column(Float, nullable=True)
    auto_category = Column(String(1), nullable=True)