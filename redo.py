import logging
import logging.config
import pickle
from sys import argv
from ctrl import Tweet_Ctrl, User_Ctrl
from utils import get_tweepy_api, get_connection, notify
from models import Tweet, User
from subprocess import run


logging.config.fileConfig(
    fname='log.conf',
    defaults={'logfilename': './logs/{}.log'.format(argv[2])}
)
logger = logging.getLogger('dev')
tweepy = get_tweepy_api()


def add_one(s, item):
    try:
        s.add(item)
        s.commit()

    except Exception as e:
        logger.error(e)
        s.rollback()


def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


def add_chunk(session, items):
    chunks = list(divide_chunks(items, 50))
    for i, chunk in enumerate(chunks):
        try :
            for item in chunk:
                session.add(item)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e)
            for item in chunk:
                add_one(session, item)
            
        logger.info('Chunk {} done'.format(i))


def get_statuses(session, tweets_ids):
    tweets = []
    users_dict = {}
    statuses = tweepy.statuses_lookup(tweets_ids, tweet_mode="extended")
    for status in statuses:
        tweets.append(ctrl_tweet.new_tweet(status))

        if status.user.id not in users_dict:
            u = ctrl_user.new_user(status.user)
            users_dict[u.id] = u

    users = [ u[1] for u in list(users_dict.items()) ]

    logger.info("Adding users")
    add_chunk(session, users)
    logger.info("Adding users done")

    logger.info("Adding tweets")
    add_chunk(session, tweets)
    logger.info("Adding tweets done")
    
    del users_dict
    del users
    del tweets
    del statuses


def process_db(db):
    _, SM1 = get_connection(db)
    s1 = SM1()

    db2 = 'r_{}'.format(db)
    _, SM2 = get_connection(db2)
    s2 = SM2()
    run(('python', 'create_db.py', db2, db2))
    logger.info('Database created')

    tweets_db = [ t[0] for t in s1.query(Tweet.id).all() ]
    tweets_id_chunks = list(divide_chunks(tweets_db, 100))
    logger.info('Got the tweets from the database')
    
    for i, til in enumerate(tweets_id_chunks):
        logger.info('Working on tweets_id_chunk {}'.format(i))
        get_statuses(s2, til)

    notify('Database {}'.format(db), 'It is done')


if __name__ == "__main__":
    logger.info('yo')

    ctrl_tweet = Tweet_Ctrl()
    ctrl_user = User_Ctrl()

    dbs = [3,5,6,7,8,9,11,12,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,30,31]
    for i in dbs:
        db = 'hta_{:02}'.format(i)
        logger.info('Working on database {}'.format(db))

        try:
            process_db(db)
        except Exception as e:
            logger.error(e)
        
    notify('Redo Done', 'Everything should be normal now')
