import pickle
import logging
import logging.config
import datetime
import tweepy
from sys import argv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import get_tweepy_api, get_db_uri


logging.config.fileConfig(
    fname='log.conf',
    defaults={'logfilename': './logs/{}.log'.format(argv[2])}
)
logger = logging.getLogger('dev')

Base = declarative_base()
database = argv[1]
engine = create_engine(get_db_uri(database))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def get_tweets(q):
    logger.info('new query: {}'.format(q))
    pg_n = 0
    n_user, n_tweets, n_retweets, n_hashtags = 0, 0, 0, 0
    for pg in tweepy.Cursor(api.search, q=q, count=100, tweet_mode="extended").pages():
        users = {}
        tweets = []
        retweets_st = []
        hashtags = []

        for s in pg:
            users[s.user.id] = user_ctrl.new_user(s.user)

            if hasattr(s, 'retweeted_status'):
                tweets.append(retweet_ctrl.get_original(s))
                retweets_st.append(s)
            else:
                tweets.append(tweet_ctrl.new_tweet(s))
        
        for us in chunkIt(list(users.items()), 2):
            us = [ x[1] for x in us ]
            user_ctrl.add_users(us)

            n = len(us)
            n_user += n
            logger.info("Added {} users".format(n))
        
        for ts in chunkIt(tweets, 2):
            tweet_ctrl.add_tweets(ts)
            
            n = len(ts)
            n_tweets += n
            logger.info("Added {} tweets".format(n))

        retweets = []
        for s in retweets_st:
            retweets.append(retweet_ctrl.new_retweet(s))

        for rt in chunkIt(retweets, 2):
            retweet_ctrl.add_retweets(rt)

            n = len(rt)
            n_retweets += n
            logger.info("Added {} retweets".format(n))

        for s in pg:
            if not hasattr(s, 'retweeted_status'):
                hashtags.extend(hashtag_ctrl.new_hashtags(s))

        for ht in chunkIt(hashtags, 2):
            hashtag_ctrl.add_hashtags(ht)

            n = len(ht)
            n_hashtags += n
            logger.info("Added {} hashtags".format(n))

        logger.info('page {} done'.format(pg_n))
        pg_n += 1

    logger.info('Hashtag {} done :3'.format(q))
    return dict(
        pg_n=pg_n, n_user=n_user, n_tweets=n_tweets,
        n_retweets=n_retweets, n_hashtags=n_hashtags
    )


def notify(hashtag, results):
    import smtplib
    import json
    from datetime import datetime

    gmail_user = 'breno.cardoso@estudante.ufla.br'
    gmail_password = 'iewjbnmnpujoavsm'

    sent_from = gmail_user
    to = ['k4t0mono@gmail.com']

    subject = 'Done {} - {}'.format(hashtag, datetime.now())
    body = """
The script is done :3

I got: {}
""".format(json.dumps(results, indent=4))

    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')


if __name__ == "__main__":
    from utils import get_tweepy_api
    from ctrl import *

    api = get_tweepy_api()
    logger.info('yo')
    user_ctrl = User_Ctrl()
    tweet_ctrl = Tweet_Ctrl()
    retweet_ctrl = Retweet_Ctrl()
    hashtag_ctrl = Hashtag_Ctrl()

    hashtag = argv[2]
    q = "#{}".format(hashtag.strip())
    result = get_tweets(q)

    notify(hashtag, result)