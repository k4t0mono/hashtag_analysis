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

if __name__ == "__main__":
    from utils import get_tweepy_api
    from ctrl import *

    api = get_tweepy_api()
    logger.info('yo')
    user_ctrl = User_Ctrl()
    tweet_ctrl = Tweet_Ctrl()

    # user = User(id=123123, screen_name='k4t0mono', created_at=datetime.datetime.now())
    # session.add(user)
    # session.commit()

    status = api.get_status(1166190484479512576)
    t = tweet_ctrl.new_tweet(status)
    tweet_ctrl.add_tweet(t)