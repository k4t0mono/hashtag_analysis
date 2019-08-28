from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from main import Base
from .User import User
from .Tweet import Tweet
from .Hashtag import Hashtag


class Retweeted(Base):
    __tablename__ = 'retweet'

    retweet_id = Column(Integer, ForeignKey('tweet.id'), primary_key=True)
    retweet = relationship(Tweet, foreign_keys=[retweet_id])

    original_tweet_id = Column(Integer, ForeignKey('tweet.id'))
    original_tweet = relationship(Tweet, foreign_keys=[original_tweet_id])


class Mention(Base):
    __tablename__ = 'mention'

    tweet_id = Column(Integer, ForeignKey('tweet.id'), primary_key=True)
    tweet = relationship(Tweet)

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship(User)


class Reply(Base):
    __tablename__ = 'reply'

    reply_id = Column(Integer, ForeignKey('tweet.id'), primary_key=True)
    reply = relationship(Tweet, foreign_keys=[reply_id])

    replyee_id = Column(Integer, ForeignKey('tweet.id'), primary_key=True)
    replyee = relationship(Tweet, foreign_keys=[replyee_id])

class HasHastag(Base):
    __tablename__ = 'HasHastag'

    tweet_id = Column(Integer, ForeignKey('tweet.id'), primary_key=True)
    tweet = relationship(Tweet)

    hashtag_name = Column(Integer, ForeignKey('hashtag.name'), primary_key=True)
    hashtag = relationship(Hashtag)