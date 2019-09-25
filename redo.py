import logging
import logging.config
import pickle
from sys import argv
from ctrl import Tweet_Ctrl
from utils import get_tweepy_api, get_connection, notify
from models import Tweet, User


logging.config.fileConfig(
    fname='log.conf',
    defaults={'logfilename': './logs/{}.log'.format(argv[2])}
)
logger = logging.getLogger('dev')
tweepy = get_tweepy_api()


if __name__ == "__main__":
    logger.info('yo')

    ctrl_tweet = Tweet_Ctrl()
    redo = pickle.load(open('redo.pkl', 'rb'))

    dbs = [1,3,5,6,7,8,9,11,12,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,30,31]

    for i in dbs:
        db = 'hta_{:02}'.format(i)
        b, s = get_connection(db, uri="mysql+pymysql://hta:Lux.3a@oxum.stuffium.tk")
        logger.info('Working on database {}'.format(db))

        tweets = []
        for i, id_ in enumerate(redo[db]):
            try:
                status = tweepy.get_status(id_, tweet_mode="extended")

            except Exception as e:
                logger.error('Raise error on {}'.format(id_))
                logger.error(e)
                continue
        
            tweets.append(ctrl_tweet.new_tweet(status))
            if (i % 5) == 0:
                s.commit()
                logger.info('I had done {}'.format(i))
        
        users_redo = [ x.user for x in tweets ]
        users_db = [ x[0] for x in s.query(User.id).all() ]
        users = [ x for x in users_redo if str(x.id) not in users_db ]
        logger.info('Got the users')

        s.bulk_save_objects(users)
        s.commit()
        logger.info('commited the users')

        tweets_db = [ x[0] for x in s.query(Tweet.id).filter(Tweet.user_id == None) ]
        tweets = [ x for x in tweets if str(x.id) in tweets_db ]
        for t in tweets:
            s.query(Tweet).filter(Tweet.id == t.id).update({'user_id': t.user.id})
        s.commit()
        logger.info('commited tweets')

        notify('Database {}'.format(db), 'It is done')

    notify('Redo Done', 'Everything should be normal now')
