from models import Tweet
from main import session, logger
from .user_ctrl import User_Ctrl


class Tweet_Ctrl():

    def __init__(self):
        self.user_ctrl = User_Ctrl()

    def new_tweet(self, status):
        # user = self.user_ctrl.get_user(status.user.id)
        return Tweet(
            id=status.id,
            text=status.text,
            favorites=status.favorite_count,
            retweets=status.retweet_count,
            created_at=status.created_at,
            user_id=status.user.id,
        )

    def add_tweet(self, tweet):
        try:
            session.add(tweet)
            session.commit()
        except Exception as e:
            logger.debug(e)
            session.rollback()
        else:
            logger.info("Added tweet {}".format(tweet.id))

    def add_tweets(self, tweet_list):
        for tweet in tweet_list:
            session.add(tweet)
        
        session.commit()