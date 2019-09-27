import logging
import logging.config
import pickle
from sys import argv
from ctrl import Tweet_Ctrl
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
    chunks = list(divide_chunks(items, 42))
    for i, chunk in enumerate(chunks):
        for item in chunk:
            session.add(item)
        session.commit()
        logger.info('Chunk {} done'.format(i))

if __name__ == "__main__":
    logger.info('yo')

    ctrl_tweet = Tweet_Ctrl()
    redo = pickle.load(open('redo.pkl', 'rb'))

    dbs = [1,3,5,6,7,8,9,11,12,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,30,31]

    for i in dbs:
        db = 'hta_{:02}'.format(i)
        b, s = get_connection(db)
        logger.info('Working on database {}'.format(db))

        db2 = 'r_{}'.format(db)
        _, s2 = get_connection(db2)
        run(('python', 'create_db.py', db2, db2))

        tweets_db = [ t.id for t in s.query(Tweet).all() ]
        logger.info('Got the tweets')

        tweets = []
        for i, id_ in enumerate(tweets_db):
            try:
                status = tweepy.get_status(id_, tweet_mode="extended")
                tweets.append(ctrl_tweet.new_tweet(status))

            except Exception as e:
                logger.error('Raise error on {}'.format(id_))
                logger.error(e)
                continue
        
            if (i % 5) == 0:
                logger.info('I had done {}'.format(i))
        
        add_chunk(s2, tweets)

        notify('Database {}'.format(db), 'It is done')

    notify('Redo Done', 'Everything should be normal now')
