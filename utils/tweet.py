class Tweet:
    
    def __init__(self, status):
        self.id = status.id
        self.favorite = status.favorite_count
        self.retweet = status.retweet_count
        self.created_at = status.created_at
        
        self.hashtags = [ x.text for x in status.entities['hashtags'] ]
        self.mentions = [ x.id for x in status.entities['user_mentions'] ]
        
        self.is_retweet = False
        if hasattr(status, 'retweeted_status'):
            self.is_retweet = True
            self.original_tweet = status.retweeted_status.id
        
        self.is_reply = False
        if status.in_reply_to_status_id:
            self.reply_to = status.in_reply_to_status_id
        
        self.is_quote = status.is_quote_status
        if status.is_quote_status:
            self.quoted = status.quoted_status_id