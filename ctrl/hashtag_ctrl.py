from models import Hashtag
from get_tweets import session, logger
from .tweet_ctrl import Tweet_Ctrl


class Hashtag_Ctrl():

    def __init__(self):
        self.tweet_ctrl = Tweet_Ctrl()

    def new_hashtags(self, status):
        t = self.tweet_ctrl.get_tweet(status.id)

        return [ Hashtag(tweet=t, hashtag=ht['text']) for ht in status.entities['hashtags'] ]

    def add_hashtag(self, hashtag):
        try:
            session.add(hashtag)
            session.commit()
        except Exception as e:
            logger.debug(e)
            session.rollback()
        else:
            logger.info("Added hashtag {}:{}".format(hashtag.hashtag, hashtag.tweet_id))

    def add_hashtags(self, hashtag_list):
        for hashtag in hashtag_list:
            if self.get_hashtag(hashtag.hashtag):
                continue
            session.add(hashtag)
        
        session.commit()

    def get_hashtag(self, hashtag):
        try:
            return session.query(Hashtag).filter(Hashtag.hashtag == hashtag).one()
        except:
            return None