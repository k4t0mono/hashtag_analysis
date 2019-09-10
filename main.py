import pickle
import logging
import logging.config
import datetime
import tweepy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import get_tweepy_api, DB_URI


with open('run', 'r') as fl:
    lines = fl.readlines()

database = lines[0].strip()
hashtags = lines[1:]

logging.config.fileConfig(fname='log.conf')
logger = logging.getLogger('dev')

Base = declarative_base()
engine = create_engine(DB_URI.replace('uwu', database))
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


def get_tweets(q):
    logger.info('new query: {}'.format(q))
    pg_n = 0
    for pg in tweepy.Cursor(api.search, q=q, count=100, tweet_mode="extended").pages(2):
        users = {}
        tweets = []
        retweets_st = []
        hashtags = []

        for s in pg:
            users[s.user.id] = user_ctrl.new_user(s.user)

            if hasattr(s, 'retweeted_status'):
                tweets.append(retweet_ctrl.get_original(s))
                retweets_st.append(s)
            else:
                tweets.append(tweet_ctrl.new_tweet(s))
        
        for us in chunkIt(list(users.items()), 5):
            us = [ x[1] for x in us ]
            user_ctrl.add_users(us)
            logger.info("Added {} users".format(len(us)))
        
        for ts in chunkIt(tweets, 5):
            tweet_ctrl.add_tweets(ts)
            logger.info("Added {} tweets".format(len(ts)))

        retweets = []
        for s in retweets_st:
            retweets.append(retweet_ctrl.new_retweet(s))

        for rt in chunkIt(retweets, 5):
            retweet_ctrl.add_retweets(rt)
            logger.info("Added {} retweets".format(len(rt)))

        for s in pg:
            if not hasattr(s, 'retweeted_status'):
                hashtags.extend(hashtag_ctrl.new_hashtags(s))

        for ht in chunkIt(hashtags, 5):
            hashtag_ctrl.add_hashtags(ht)
            logger.info("Added {} hashtags".format(len(ht)))

        logger.info('page {} done'.format(pg_n))
        pg_n += 1

    logger.info('Hashtag {} done :3'.format(q))


if __name__ == "__main__":
    from utils import get_tweepy_api
    from ctrl import *

    api = get_tweepy_api()
    logger.info('yo')
    user_ctrl = User_Ctrl()
    tweet_ctrl = Tweet_Ctrl()
    retweet_ctrl = Retweet_Ctrl()
    hashtag_ctrl = Hashtag_Ctrl()

    for hashtag in hashtags:
        q = "#{}".format(hashtag.strip())
        get_tweets(q)