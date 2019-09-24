import logging
import logging.config
import pickle
from utils import get_botometer, get_connection
from sys import argv
from sqlalchemy import Column, ForeignKey, Float, String


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
    try:
        r = botometer.check_account(user)
    except Exception as e:
        logger.error(e)
        return -1, -1


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

    users_todo = pickle.load(open('users_todo.pkl', 'rb'))
    users_done = pickle.load(open('users_done.pkl', 'rb'))

    n_done = 0
    logger.info('I have {} users to get'.format(len(users_todo)))
    logger.info('I\' done {} users'.format(len(users_done)))

    try:
        for i, user in enumerate(users_todo[:250]):
            if(i % 5 == 0):
                logger.info('I did {} more'.format(n_done))
                s_master.commit()
            
            score, cat = get_universal_score(user)

            ub = UBot(id=user, score=score, category=cat)
            s_master.add(ub)
            n_done += 1

    except Exception as e:
        logger.error(e)
    
    finally:
        users_done.extend(users_todo[:n_done])

        pickle.dump(users_todo[n_done:], open('users_todo.pkl', 'wb'))
        pickle.dump(users_done, open('users_done.pkl', 'wb'))

        notify()