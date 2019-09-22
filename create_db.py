import models
from sys import argv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base
from utils import get_db_uri


if __name__ == "__main__":
    database = argv[1]

    engine_create = create_engine(get_db_uri(''))
    DBSession = sessionmaker(bind=engine_create)
    session = DBSession()

    session.execute('drop database if exists {};'.format(database))
    session.execute('create database {} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ;'.format(database))

    Base.metadata.create_all(create_engine(get_db_uri(database)))
