import logging
import logging.config
import pickle
from utils import get_botometer, get_connection, notify
from sys import argv
from sqlalchemy import Column, ForeignKey, Float, String
from datetime import datetime


b, SM = get_connection('ubot')
SESSION = SM()


class UBot(b):
    __tablename__ = 'ubot'
    
    id = Column(String(128), primary_key=True)
    score = Column(Float, nullable=False)
    category = Column(String(1), nullable=False)

logging.config.fileConfig(
    fname='log.conf',
    defaults={'logfilename': './logs/{}.log'.format(argv[2])}
)
logger = logging.getLogger('dev')
botometer = get_botometer()


def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


def get_universal_score(result):
    score = result['scores']['universal']

    if (score <= 0.2):
        return score, 0
    elif (score > 0.2) and (score <= 0.4):
        return score, 1
    elif (score > 0.4) and (score <= 0.6):
        return score, 2
    elif (score > 0.6) and (score <= 0.8):
        return score, 3
    elif (score > 0.8) and (score <= 1.0):
        return score, 4
    else:
        return score, '?'

def add_one(item):
    try:
        SESSION.add(item)
        SESSION.commit()
    except Exception as e:
        logger.error(e)
        SESSION.rollback()

def process_chunk(chunk):
    users = []
    for user, result in botometer.check_accounts_in(chunk):
        try:
            score, cat = get_universal_score(result)
            users.append(UBot(id=user, score=score, category=cat))
        except Exception as e:
            logger.error(e)
            logger.error(result)
            continue

    logger.info('got users')

    try:
        for u in users:
            SESSION.add(u)
        SESSION.commit()
    except Exception as e:
        logger.error(e)
        SESSION.rollback()

        for u in users:
            add_one(u)
    finally:
        logger.info('saved users')

if __name__ == "__main__":
    logger.info('yo')

    users_todo = pickle.load(open('users_todo.pkl', 'rb'))
    users_done = pickle.load(open('users_done.pkl', 'rb'))

    logger.info('I have {} users to get'.format(len(users_todo)))
    logger.info('I have done {} users'.format(len(users_done)))

    CHUNK_SIZE = 5
    chunks_base = list(divide_chunks(users_todo, 20_000))
    chunks = list(divide_chunks(chunks_base[0], CHUNK_SIZE))
    n_chunks = len(chunks)

    n_done = 0
    try:
        for i, chunk in enumerate(chunks):
            process_chunk(chunk)
            users_done.extend(chunk)
            n_done += CHUNK_SIZE

            logger.info('chunk {:04}/{:04} done'.format(i, n_chunks))

        logger.info('Done for today :3')

    except Exception as e:
        logger.error(e)
        notify
    
    finally:
        pickle.dump(users_todo[n_done:], open('users_todo.pkl', 'wb'))
        pickle.dump(users_done, open('users_done.pkl', 'wb'))

        notify(
            'Botometer of {}'.format(datetime.now()),
            'I got {} today'.format(n_done)
        )