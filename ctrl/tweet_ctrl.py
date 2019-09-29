from models import Tweet
from get_tweets import session, logger
from .user_ctrl import User_Ctrl


class Tweet_Ctrl():

    def __init__(self):
        self.user_ctrl = User_Ctrl()

    def new_tweet(self, status):
        # u = self.user_ctrl.new_user(status.user)
        
        return Tweet(
            id=status.id,
            text=status.full_text,
            favorites=status.favorite_count,
            retweets=status.retweet_count,
            created_at=status.created_at,
            user_id=status.user.id,
            is_quote=status.is_quote_status,
            in_reply=status.in_reply_to_status_id,
            mentions=len(status.entities['user_mentions']),
            hashtags=len(status.entities['hashtags']),
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
            if self.get_tweet(tweet.id):
                continue
            if len(tweet.text) > 500:
                continue

            session.add(tweet)
        
        session.commit()
    
    def get_tweet(self, id_):
        try:
            return session.query(Tweet).filter(Tweet.id == id_).one()
        except:
            return None
