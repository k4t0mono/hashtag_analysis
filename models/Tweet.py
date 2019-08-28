from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from main import Base
from .User import User


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    text = Column(String(280), nullable=False)
    favorites = Column(Integer, nullable=False)
    retweets = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)