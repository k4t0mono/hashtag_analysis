import os
import tweepy

def get_tweepy_api():
    HA_CK = os.environ.get('HA_CK')
    HA_CS = os.environ.get('HA_CS')
    HA_AT = os.environ.get('HA_AT')
    HA_TS = os.environ.get('HA_TS')

    auth = tweepy.OAuthHandler(HA_CK, HA_CS)
    auth.set_access_token(HA_AT, HA_TS)

    return tweepy.API(auth, wait_on_rate_limit=True)

database = input('database: /')
DB_URI = '{}/{}'.format(os.environ.get('DB_URI'), database)