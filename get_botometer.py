import logging
import pickle
from get_tweets import Base, session
from utils import get_botometer
from sys import argv
from sqlalchemy import Column, ForeignKey, Float, String
from utils import get_connection


b, s_master = get_connection('ubot')
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


def notify():
    import smtplib
    import json
    from datetime import datetime

    gmail_user = 'breno.cardoso@estudante.ufla.br'
    gmail_password = 'iewjbnmnpujoavsm'

    sent_from = gmail_user
    to = ['k4t0mono@gmail.com']

    subject = 'Done botometer chunk'
    body = 'The script is done :3'

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


def get_universal_score(user):
    r = botometer.check_account(user)

    score = r['scores']['universal']

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
        return score, 99


if __name__ == "__main__":
    logger.info('yo')

    chunks = pickle.load(open('users_chunks.pkl', 'rb'))
    if not len(chunks):
        notify()
        logger.info('nothing more to do')
        exit(0)

    chunk = chunks[0]
    for u in chunk[:3]:
        score, cat = get_universal_score(u)

        logger.info('User {} : {:.2f} - {}'.format(u, score, cat))

        ub = UBot(id=u, score=score, category=cat)
        s_master.add(ub)
        s_master.commit()
    
    pickle.dump(chunks[1:], open('users_chunks.pkl', 'wb'))
    logger.info('chunk done')
    notify()