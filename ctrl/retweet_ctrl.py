from models import Retweet
from main import session, logger
from .tweet_ctrl import Tweet_Ctrl
from .user_ctrl import User_Ctrl


class Retweet_Ctrl():

    def __init__(self):
        self.tweet_ctrl = Tweet_Ctrl()
        self.user_ctrl = User_Ctrl()

    def get_original(self, status):
        return self.tweet_ctrl.new_tweet(status.retweeted_status)

    def new_retweet(self, status):
        ot_id = status.retweeted_status.id
        user = self.user_ctrl.get_user(status.user.id)

        return Retweet(
            id=status.id,
            created_at=status.created_at,
            original_tweet_id=ot_id,
            user=user,
        )
    
    def add_retweet(self, retweet):
        try:
            session.add(retweet)
            session.commit()
        except Exception as e:
            logger.debug(e)
            session.rollback()
        else:
            logger.info("Added retweet {}".format(retweet.id))

    def add_retweets(self, retweet_list):
        for retweet in retweet_list:
            if self.get_retweet(retweet.id):
                continue

            session.add(retweet)
        
        try:
            session.commit()
        except Exception as e:
            logger.debug(e)
            session.rollback()

            for rt in retweet_list:
                self.add_retweet(rt)
    
    def get_retweet(self, id_):
        try:
            return session.query(Retweet).filter(Retweet.id == id_).one()
        except:
            return None