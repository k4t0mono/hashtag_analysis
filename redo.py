import logging
import logging.config
import pickle
from sys import argv
from ctrl import Tweet_Ctrl
from utils import get_tweepy_api, get_connection, notify
from models import Tweet


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

    for i in range(1, 32):
        db = 'hta_{:02}'.format(i)
        _, s = get_connection(db, uri="mysql+pymysql://hta:Lux.3a@oxum.stuffium.tk")
        logger.info('Working on database {}'.format(db))

        for i, id_ in enumerate(redo[db]):
            try:
                status = tweepy.get_status(id_, tweet_mode="extended")
                t = ctrl_tweet.new_tweet(status)
                s.add(t.user)
                s.query(Tweet).filter(Tweet.id == t.id).update({'user_id': t.user.id})

            except Exception as e:
                logger.error('Raise error on {}'.format(id_))
                logger.error(e)
                s.rollback()
                continue
        
            if (i % 10) == 0:
                s.commit()
                logger.info('I had done {}'.format(i))
        
        notify('Database {}'.format(db), 'It is done')

    notify('Redo Done', 'Everything should be normal now')
