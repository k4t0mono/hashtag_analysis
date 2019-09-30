import os
import tweepy
import botometer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def get_botometer():
    HA_CK = os.environ.get('HA_CK')
    HA_CS = os.environ.get('HA_CS')
    HA_AT = os.environ.get('HA_AT')
    HA_TS = os.environ.get('HA_TS')
    HA_BO = os.environ.get('HA_BO')

    twitter_auth = dict(
        consumer_key=HA_CK, consumer_secret=HA_CS,
        access_token=HA_AT, access_token_secret=HA_TS
    )

    return botometer.Botometer(
        wait_on_ratelimit=True, rapidapi_key=HA_BO, **twitter_auth
    )

def get_tweepy_api():
    HA_CK = os.environ.get('HA_CK')
    HA_CS = os.environ.get('HA_CS')
    HA_AT = os.environ.get('HA_AT')
    HA_TS = os.environ.get('HA_TS')

    auth = tweepy.OAuthHandler(HA_CK, HA_CS)
    auth.set_access_token(HA_AT, HA_TS)

    return tweepy.API(auth, wait_on_rate_limit=True)


def get_db_uri(database, **kwargs):
    uri = os.environ.get('DB_URI')
    if kwargs:
        uri = kwargs.get('uri')


    return '{}/{}?charset=utf8mb4'.format(uri, database)

def get_connection(database, **kwargs):
    base = declarative_base()
    engine = create_engine(get_db_uri(database, **kwargs))
    base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)

    return (base, DBSession)