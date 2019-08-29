import models
from sqlalchemy import create_engine
from main import Base, engine


Base.metadata.create_all(engine)