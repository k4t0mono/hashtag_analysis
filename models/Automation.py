from sqlalchemy import Column, ForeignKey, String, Float, Integer
from sqlalchemy.orm import relationship
from get_tweets import Base
from .User import User


class Automation(Base):
    __tablename__ = 'automation'

    user_id = Column(String(128), ForeignKey('user.id'), primary_key=True)
    user = relationship(User)

    score = Column(Float, nullable=True)
    category = Column(String(1), nullable=True)
