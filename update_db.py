import logging
import logging.config
import pickle
from datetime import datetime
from utils import get_connection, Progress
from models import User
from sqlalchemy import Column, ForeignKey, Float, String


logging.config.fileConfig(
    fname='log.conf',
    defaults={'logfilename': './logs/{}.log'.format(argv[2])}
)
logger = logging.getLogger('dev')


b, sm1 = get_connection('ubot', uri='mysql+pymysql://hta:Lux.3a@oxum.stuffium.tk')
s1 = sm1()


class UBot(b):
    __tablename__ = 'ubot'

    id = Column(String(128), primary_key=True)
    score = Column(Float, nullable=False)
    category = Column(String(1), nullable=False)


def update_user(user_id, s1, s2):
    ub = s1.query(UBot).filter(UBot.id == user_id).first()

    if not ub:
        return False

    s2\
        .query(User)\
        .filter(User.id == user_id)\
        .update({ User.auto_score: ub.score, User.auto_category: ub.category })

    return True


def update_db(db):
    users_todo = []

    _, sm2 = get_connection(db, uri='mysql+pymysql://hta:Lux.3a@oxum.stuffium.tk')
    s2 = sm2()
    users = s2.query(User.id).filter(User.auto_score == None).all()[:5]

    for i, (u,) in enumerate(users):
        if not update_user(u, s1, s2):
            users_todo.append(u)

        if i%10 == 0:
            logger.info('{} done in {}'.format(i, db))

    print()
    return users_todo


if __name__ == '__main__':
    users_todo = []
    for i in range(1, 35):
        db = 'r_hta_{:02}'.format(i)
        logger.info('starting {}'.format(db))
        try:
            ut = update_db(db)
            users_todo.extend(ut)
        except Exception as e:
            print(db, e)

        logger.info('done {}'.format(db))

    dt = datetime.now()
    t = '{}{}{}_{:02}{:02}{:02}'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    pickle.dump(users_todo, open('user_todo_{}.pkl'.format(t), 'wb'))
