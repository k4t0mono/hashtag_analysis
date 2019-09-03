from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from main import Base
from .User import User
from .Tweet import Tweet


class Retweet(Base):
    __tablename__ = 'retweet'

    id = Column(String(128), primary_key=True)
    created_at = Column(DateTime, nullable=False)

    original_tweet_id = Column(String(128), ForeignKey('tweet.id'))
    original_tweet = relationship(Tweet, foreign_keys=[original_tweet_id])

    user_id = Column(String(128), ForeignKey('user.id'))
    user = relationship(User)


class Mention(Base):
    __tablename__ = 'mention'

    tweet_id = Column(String(128), ForeignKey('tweet.id'), primary_key=True)
    tweet = relationship(Tweet)

    user_id = Column(String(128), ForeignKey('user.id'), primary_key=True)
    user = relationship(User)


class Reply(Base):
    __tablename__ = 'reply'

    reply_id = Column(String(128), ForeignKey('tweet.id'), primary_key=True)
    reply = relationship(Tweet, foreign_keys=[reply_id])

    replyee_id = Column(String(128), ForeignKey('tweet.id'), primary_key=True)
    replyee = relationship(Tweet, foreign_keys=[replyee_id])

class Hashtag(Base):
    __tablename__ = 'hashtags'

    tweet_id = Column(String(128), ForeignKey('tweet.id'), primary_key=True)
    tweet = relationship(Tweet)

    hashtag = Column(String(140), primary_key=True)
