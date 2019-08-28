import pickle
import logging
import logging.config
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import get_tweepy_api


logging.config.fileConfig(fname='log.conf')
logger = logging.getLogger('dev')

Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


if __name__ == "__main__":
    from utils import get_tweepy_api
    from ctrl import *

    api = get_tweepy_api()
    logger.info('yo')
    user_ctrl = User_Ctrl()
    tweet_ctrl = Tweet_Ctrl()

    users = {}
    tweets = []
    for s in api.search('#panelaço', count=100):
        users[s.user.id] = user_ctrl.new_user(s.user)
        tweets.append(tweet_ctrl.new_tweet(s))
    
    
    for us in chunkIt(list(users.items()), 5):
        us = [ x[1] for x in us ]
        user_ctrl.add_users(us)
        logger.info("Added {} users".format(len(us)))
    
    for ts in chunkIt(tweets, 5):
        tweet_ctrl.add_tweets(ts)
        logger.info("Added {} tweets".format(len(ts)))