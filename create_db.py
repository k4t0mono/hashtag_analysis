import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, engine, database


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

session.execute('drop database if exists {};'.format(database))
session.execute('create database {} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ;'.format(database))

Base.metadata.create_all(engine)