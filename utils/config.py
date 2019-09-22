import os
import tweepy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def get_tweepy_api():
    HA_CK = os.environ.get('HA_CK')
    HA_CS = os.environ.get('HA_CS')
    HA_AT = os.environ.get('HA_AT')
    HA_TS = os.environ.get('HA_TS')

    auth = tweepy.OAuthHandler(HA_CK, HA_CS)
    auth.set_access_token(HA_AT, HA_TS)

    return tweepy.API(auth, wait_on_rate_limit=True)


def get_db_uri(database):
    return '{}/{}?charset=utf8mb4'.format(os.environ.get('DB_URI'), database)

def get_connection(database):
    base = declarative_base()
    engine = create_engine(get_db_uri(database))
    base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return (base, session)