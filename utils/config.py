import os
import tweepy
from gremlin_python.driver import client, serializer

HA_CK = os.environ.get('HA_CK')
HA_CS = os.environ.get('HA_CS')
HA_AT = os.environ.get('HA_AT')
HA_TS = os.environ.get('HA_TS')

auth = tweepy.OAuthHandler(HA_CK, HA_CS)
auth.set_access_token(HA_AT, HA_TS)

api = tweepy.API(auth, wait_on_rate_limit=True)

GREMLIN_URI = os.environ.get('GREMLIN_URI')
GREMLIN_KEY = os.environ.get('GREMLIN_KEY')
client = client.Client(GREMLIN_URI, 'g', 
    username='/dbs/dm_project/colls/tweets', 
    password=GREMLIN_KEY,
    message_serializer=serializer.GraphSONSerializersV2d0()
)